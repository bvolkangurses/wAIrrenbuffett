#!/usr/bin/env python3
"""
wAIrrenbuffett - AI-Assisted Financial Planner
Main application entry point
"""
import sys
import argparse
from user_profile import UserProfile, collect_user_profile
from market_data import MarketDataFetcher
from ai_advisor import AIAdvisor
from financial_projections import FinancialProjector
from demo import get_demo_profile, print_demo_info
from fallback_stocks import get_fallback_stock_data


def print_section_header(title: str):
    """Print a formatted section header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")


def print_profile_summary(profile: UserProfile):
    """Print user profile summary"""
    print_section_header("YOUR FINANCIAL PROFILE")
    print(f"Age: {profile.age} | Location: {profile.location}")
    print(f"Career: {profile.career_field}")
    print(f"Years to Retirement: {profile.years_to_retirement}")
    print(f"\nFinancial Snapshot:")
    print(f"  Annual Income:     ${profile.annual_income:,.2f}")
    print(f"  Current Savings:   ${profile.current_savings:,.2f}")
    print(f"  Monthly Expenses:  ${profile.monthly_expenses:,.2f}")
    print(f"  Total Debt:        ${profile.total_debt:,.2f}")
    print(f"\nInvestment Profile:")
    print(f"  Risk Tolerance:    {profile.risk_tolerance.capitalize()}")
    print(f"  Investment Horizon: {profile.investment_horizon} years")
    if profile.preferred_sectors:
        print(f"  Preferred Sectors: {', '.join(profile.preferred_sectors)}")


def print_analysis(analysis: dict):
    """Print AI analysis results"""
    print_section_header("AI FINANCIAL ANALYSIS")
    
    health = analysis['financial_health']
    print("Financial Health Metrics:")
    print(f"  Savings Rate:          {health['savings_rate']:.1f}%")
    print(f"  Debt-to-Income Ratio:  {health['debt_to_income_ratio']:.1f}%")
    print(f"  Emergency Fund:        {health['emergency_fund_months']:.1f} months")
    if health['years_to_debt_free'] != 'N/A':
        print(f"  Years to Debt Free:    {health['years_to_debt_free']:.1f} years")
    
    print(f"\n{analysis['risk_assessment']}")
    print(f"\nRecommended Strategy: {analysis['investment_strategy']}")
    
    allocation = analysis['recommended_allocation']
    print(f"\nRecommended Asset Allocation:")
    print(f"  Stocks: {allocation['stocks']:.1f}% | Bonds: {allocation['bonds']:.1f}%")
    print(f"  Breakdown:")
    for asset_type, pct in allocation['breakdown'].items():
        print(f"    {asset_type.replace('_', ' ').title()}: {pct:.1f}%")


def print_stock_recommendations(recommendations: list):
    """Print stock recommendations"""
    print_section_header("PERSONALIZED STOCK PICKS")
    
    if not recommendations:
        print("No recommendations available at this time.")
        return
    
    print(f"Top {len(recommendations)} Stock Recommendations:\n")
    
    for i, stock in enumerate(recommendations, 1):
        print(f"{i}. {stock['ticker']} - {stock['name']}")
        print(f"   Sector: {stock['sector']}")
        print(f"   Current Price: ${stock['current_price']:.2f}")
        if stock['dividend_yield']:
            print(f"   Dividend Yield: {stock['dividend_yield']*100:.2f}%")
        if stock['pe_ratio']:
            print(f"   P/E Ratio: {stock['pe_ratio']:.2f}")
        print(f"   Score: {stock['score']:.1f}/100")
        print(f"   Why: {stock['rationale']}")
        print()


def print_projections(summary: dict, detailed_projections: dict):
    """Print financial projections"""
    print_section_header("COMPREHENSIVE FINANCIAL PROJECTIONS")
    
    current = summary['current_snapshot']
    future = summary['future_projection']
    growth = summary['growth']
    
    print("Current Snapshot:")
    print(f"  Age: {current['age']}")
    print(f"  Net Worth: ${current['net_worth']:,.2f}")
    print(f"  Annual Income: ${current['annual_income']:,.2f}")
    
    print(f"\nProjection for {future['years_ahead']} Years Ahead:")
    print(f"  Age: {future['age']}")
    print(f"  Net Worth: ${future['net_worth']:,.2f}")
    print(f"  Annual Income: ${future['annual_income']:,.2f}")
    print(f"  Annual Dividend Income: ${future['annual_dividend']:,.2f}")
    
    print(f"\nGrowth Summary:")
    print(f"  Net Worth Growth: {growth['net_worth_growth']:.1f}%")
    print(f"  Income Growth: {growth['income_growth']:.1f}%")
    
    # Retirement readiness
    retirement = summary['retirement_outlook']
    print(f"\nRetirement Readiness:")
    print(f"  Projected Net Worth at Retirement: ${retirement['retirement_net_worth']:,.2f}")
    print(f"  Estimated Annual Expenses: ${retirement['estimated_annual_expenses']:,.2f}")
    print(f"  Safe Annual Withdrawal (4% rule): ${retirement['safe_annual_withdrawal']:,.2f}")
    print(f"  Income Replacement Ratio: {retirement['replacement_ratio']:.1f}%")
    print(f"  Retirement Goal: ${retirement['retirement_goal']:,.2f}")
    
    if retirement['on_track']:
        print(f"  Status: ✓ On track for retirement!")
        if retirement['surplus_shortfall'] > 0:
            print(f"  Projected surplus: ${retirement['surplus_shortfall']:,.2f}")
    else:
        print(f"  Status: ⚠ Below retirement goal")
        print(f"  Shortfall: ${abs(retirement['surplus_shortfall']):,.2f}")
    
    # Show year-by-year projections for first 10 years
    print("\n" + "-" * 70)
    print("Detailed 10-Year Net Worth Projection:")
    print("-" * 70)
    print(f"{'Year':<6} {'Age':<6} {'Net Worth':<18} {'Annual Income':<18} {'Savings':<15}")
    print("-" * 70)
    
    for proj in detailed_projections['net_worth'][:11]:
        print(f"{proj['year']:<6} {proj['age']:<6} "
              f"${proj['net_worth']:>15,.2f}  "
              f"${proj['annual_income']:>15,.2f}  "
              f"${proj['annual_savings']:>13,.2f}")


def print_dividend_projection(dividend_projections: list):
    """Print dividend income projections"""
    print("\n" + "-" * 70)
    print("Dividend Income Projection (First 10 Years):")
    print("-" * 70)
    print(f"{'Year':<6} {'Age':<6} {'Portfolio Value':<18} {'Annual Dividend':<18}")
    print("-" * 70)
    
    for proj in dividend_projections[:11]:
        print(f"{proj['year']:<6} {proj['age']:<6} "
              f"${proj['portfolio_value']:>15,.2f}  "
              f"${proj['annual_dividend']:>15,.2f}")


def run_interactive_mode(demo_scenario=None):
    """Run the application in interactive mode"""
    print("\n")
    print("╔════════════════════════════════════════════════════════════════════╗")
    print("║                                                                    ║")
    print("║           wAIrrenbuffett - AI Financial Planner                    ║")
    print("║                                                                    ║")
    print("║     Personalized stock picks and financial projections            ║")
    print("║     powered by AI and market analysis                             ║")
    print("║                                                                    ║")
    print("╚════════════════════════════════════════════════════════════════════╝")
    print("\n")
    
    # Step 1: Collect user profile
    if demo_scenario:
        print_demo_info(demo_scenario)
        profile = get_demo_profile(demo_scenario)
    else:
        profile = collect_user_profile()
    
    # Step 2: Display profile summary
    print_profile_summary(profile)
    
    # Step 3: Initialize components
    print("\nInitializing AI advisor and fetching market data...")
    ai_advisor = AIAdvisor(use_ollama=False)
    market_data = MarketDataFetcher()
    projector = FinancialProjector()
    
    # Step 4: Analyze profile
    print("Analyzing your financial profile...")
    analysis = ai_advisor.analyze_profile(profile)
    print_analysis(analysis)
    
    # Step 5: Fetch stock data and generate recommendations
    print("\nFetching market data and generating stock recommendations...")
    print("(This may take a moment...)")
    
    # Get stocks from preferred sectors
    all_stocks = []
    for sector in profile.preferred_sectors:
        tickers = market_data.get_sector_stocks(sector, limit=5)
        all_stocks.extend(tickers)
    
    # Add dividend stocks if conservative
    if profile.risk_tolerance == 'conservative':
        all_stocks.extend(market_data.get_dividend_stocks(limit=10))
    
    # Add major blue chips
    all_stocks.extend(['AAPL', 'MSFT', 'GOOGL', 'JNJ', 'JPM', 'V', 'WMT', 'PG'])
    
    # Remove duplicates
    all_stocks = list(set(all_stocks))
    
    # Fetch detailed stock info
    stock_data = []
    fetch_errors = 0
    for ticker in all_stocks[:30]:  # Limit to 30 to avoid rate limits
        data = market_data.get_stock_info(ticker)
        if data:
            stock_data.append(data)
        else:
            fetch_errors += 1
    
    # Use fallback data if market data is unavailable
    if not stock_data or fetch_errors > 10:
        print("Note: Using demonstration data due to network limitations.")
        stock_data = get_fallback_stock_data()
    
    # Generate recommendations
    recommendations = ai_advisor.generate_stock_recommendations(
        profile, stock_data, num_picks=10
    )
    print_stock_recommendations(recommendations)
    
    # Step 6: Generate financial projections
    print("\nGenerating comprehensive financial projections...")
    
    allocation = analysis['recommended_allocation']
    
    net_worth_proj = projector.project_net_worth(profile, allocation)
    income_proj = projector.project_income(profile)
    dividend_proj = projector.project_dividends(profile, recommendations)
    portfolio_proj = projector.project_portfolio_returns(profile, allocation)
    
    all_projections = {
        'net_worth': net_worth_proj,
        'income': income_proj,
        'dividends': dividend_proj,
        'portfolio_returns': portfolio_proj
    }
    
    retirement_readiness = projector.calculate_retirement_readiness(
        profile, net_worth_proj
    )
    all_projections['retirement_readiness'] = retirement_readiness
    
    summary = projector.generate_summary(profile, all_projections)
    
    # Step 7: Display projections
    print_projections(summary, all_projections)
    print_dividend_projection(dividend_proj)
    
    # Final message
    print("\n" + "=" * 70)
    print("                    ANALYSIS COMPLETE")
    print("=" * 70)
    print("\nThank you for using wAIrrenbuffett!")
    print("\nDisclaimer: This analysis is for educational purposes only.")
    print("Always consult with a qualified financial advisor before making")
    print("investment decisions.")
    print()


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='wAIrrenbuffett - AI-Assisted Financial Planner',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Demo scenarios:
  young        - Young professional (28, aggressive investor)
  moderate     - Mid-career with family (38, balanced approach)
  conservative - Pre-retirement (52, conservative strategy)
  retirement   - Recently retired (67, income focused)

Examples:
  python main.py                    # Interactive mode
  python main.py --demo moderate    # Run with moderate demo profile
        """
    )
    parser.add_argument(
        '--demo',
        type=str,
        nargs='?',
        const='moderate',
        choices=['young', 'moderate', 'conservative', 'retirement'],
        help='Run with demo data (default: moderate)'
    )
    
    args = parser.parse_args()
    
    try:
        run_interactive_mode(demo_scenario=args.demo)
        return 0
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        return 1
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
