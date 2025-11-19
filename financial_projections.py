"""
Financial Projections Module - Calculates future financial projections
"""
from typing import List, Dict
from user_profile import UserProfile
import numpy as np


class FinancialProjector:
    """Generates comprehensive financial projections"""
    
    def __init__(self):
        self.inflation_rate = 0.03  # 3% annual inflation
        self.market_return_estimates = {
            'conservative': 0.05,
            'moderate': 0.07,
            'aggressive': 0.09
        }
    
    def project_net_worth(self, profile: UserProfile, 
                          portfolio_allocation: Dict,
                          years: int = None) -> List[Dict]:
        """Project net worth over time"""
        if years is None:
            years = min(profile.years_to_retirement, 30)
        
        projections = []
        
        # Initial values
        current_net_worth = profile.current_savings - profile.total_debt
        annual_income = profile.annual_income
        annual_expenses = profile.monthly_expenses * 12
        
        # Expected return based on allocation and risk tolerance
        expected_return = self.market_return_estimates.get(
            profile.risk_tolerance, 0.07
        )
        
        # Calculate annual savings
        annual_savings = annual_income - annual_expenses
        
        for year in range(years + 1):
            # Apply income growth
            if year > 0:
                annual_income *= (1 + profile.expected_income_growth / 100)
                annual_expenses *= (1 + self.inflation_rate)
                annual_savings = annual_income - annual_expenses
            
            # Calculate investment returns
            if year > 0:
                investment_return = current_net_worth * expected_return
                current_net_worth += investment_return + annual_savings
            
            projections.append({
                'year': year,
                'age': profile.age + year,
                'net_worth': round(current_net_worth, 2),
                'annual_income': round(annual_income, 2),
                'annual_expenses': round(annual_expenses, 2),
                'annual_savings': round(annual_savings, 2)
            })
        
        return projections
    
    def project_income(self, profile: UserProfile, years: int = None) -> List[Dict]:
        """Project income growth over time"""
        if years is None:
            years = min(profile.years_to_retirement, 30)
        
        projections = []
        annual_income = profile.annual_income
        
        for year in range(years + 1):
            if year > 0:
                annual_income *= (1 + profile.expected_income_growth / 100)
            
            projections.append({
                'year': year,
                'age': profile.age + year,
                'gross_income': round(annual_income, 2),
                'monthly_income': round(annual_income / 12, 2)
            })
        
        return projections
    
    def project_dividends(self, profile: UserProfile, 
                         stock_recommendations: List[Dict],
                         years: int = None) -> List[Dict]:
        """Project dividend income over time"""
        if years is None:
            years = min(profile.years_to_retirement, 30)
        
        # Calculate initial investment allocation to dividend stocks
        stock_allocation_pct = 0.60  # 60% of portfolio in stocks
        dividend_stock_pct = 0.40  # 40% of stocks in dividend-paying stocks
        
        initial_investment = profile.current_savings * stock_allocation_pct * dividend_stock_pct
        
        # Average dividend yield from recommendations
        avg_dividend_yield = 0.03  # Default 3%
        if stock_recommendations:
            total_yield = sum(s.get('dividend_yield', 0.03) for s in stock_recommendations)
            avg_dividend_yield = total_yield / len(stock_recommendations)
        
        # Assume 5% annual dividend growth
        dividend_growth_rate = 0.05
        
        projections = []
        current_portfolio_value = initial_investment
        annual_contributions = (profile.annual_income - profile.monthly_expenses * 12) * stock_allocation_pct * dividend_stock_pct
        
        for year in range(years + 1):
            if year > 0:
                # Portfolio grows with market and contributions
                current_portfolio_value *= 1.07  # Market appreciation
                current_portfolio_value += annual_contributions
            
            annual_dividend = current_portfolio_value * avg_dividend_yield
            
            # Dividend growth
            if year > 0:
                avg_dividend_yield *= (1 + dividend_growth_rate)
            
            projections.append({
                'year': year,
                'age': profile.age + year,
                'portfolio_value': round(current_portfolio_value, 2),
                'annual_dividend': round(annual_dividend, 2),
                'monthly_dividend': round(annual_dividend / 12, 2),
                'dividend_yield': round(avg_dividend_yield * 100, 2)
            })
        
        return projections
    
    def project_portfolio_returns(self, profile: UserProfile,
                                  allocation: Dict,
                                  years: int = None) -> List[Dict]:
        """Project expected portfolio returns"""
        if years is None:
            years = min(profile.years_to_retirement, 30)
        
        # Expected returns by asset class
        stock_return = 0.10
        bond_return = 0.04
        
        # Calculate blended return
        stock_pct = allocation['stocks'] / 100
        bond_pct = allocation['bonds'] / 100
        expected_annual_return = (stock_pct * stock_return + bond_pct * bond_return)
        
        # Volatility (standard deviation)
        stock_volatility = 0.18
        bond_volatility = 0.05
        portfolio_volatility = (stock_pct * stock_volatility + bond_pct * bond_volatility)
        
        projections = []
        current_value = profile.current_savings
        annual_contribution = profile.annual_income - profile.monthly_expenses * 12
        
        for year in range(years + 1):
            # Calculate different scenarios
            if year > 0:
                # Expected case
                expected_return = current_value * expected_annual_return
                current_value += expected_return + annual_contribution
                
                # Best case (expected + 1.5 std dev)
                best_case = current_value * (1 + 1.5 * portfolio_volatility)
                
                # Worst case (expected - 1.5 std dev)
                worst_case = current_value * (1 - 1.5 * portfolio_volatility)
                
                # Conservative case (half the expected return)
                conservative = current_value * 0.85
            else:
                best_case = current_value * 1.1
                worst_case = current_value * 0.9
                conservative = current_value
            
            projections.append({
                'year': year,
                'age': profile.age + year,
                'expected_value': round(current_value, 2),
                'best_case': round(best_case, 2),
                'worst_case': round(worst_case, 2),
                'conservative_case': round(conservative, 2),
                'total_contributions': round(annual_contribution * year, 2)
            })
        
        return projections
    
    def calculate_retirement_readiness(self, profile: UserProfile,
                                      net_worth_projections: List[Dict]) -> Dict:
        """Calculate retirement readiness metrics"""
        
        # Get net worth at retirement
        retirement_year = profile.years_to_retirement
        if retirement_year >= len(net_worth_projections):
            retirement_net_worth = net_worth_projections[-1]['net_worth']
        else:
            retirement_net_worth = net_worth_projections[retirement_year]['net_worth']
        
        # Estimate retirement expenses (80% of current expenses, adjusted for inflation)
        years_to_retirement = profile.years_to_retirement
        retirement_expenses = profile.monthly_expenses * 12 * 0.80
        retirement_expenses *= (1 + self.inflation_rate) ** years_to_retirement
        
        # 4% rule - safe withdrawal rate
        safe_annual_withdrawal = retirement_net_worth * 0.04
        
        # Years the portfolio will last
        if retirement_expenses > 0:
            replacement_ratio = (safe_annual_withdrawal / retirement_expenses) * 100
        else:
            replacement_ratio = 100
        
        # How much is needed (25x annual expenses)
        retirement_goal = retirement_expenses * 25
        
        return {
            'retirement_net_worth': round(retirement_net_worth, 2),
            'estimated_annual_expenses': round(retirement_expenses, 2),
            'safe_annual_withdrawal': round(safe_annual_withdrawal, 2),
            'replacement_ratio': round(replacement_ratio, 1),
            'retirement_goal': round(retirement_goal, 2),
            'on_track': retirement_net_worth >= retirement_goal * 0.8,
            'surplus_shortfall': round(retirement_net_worth - retirement_goal, 2)
        }
    
    def generate_summary(self, profile: UserProfile,
                        projections: Dict) -> Dict:
        """Generate comprehensive financial summary"""
        
        net_worth_proj = projections['net_worth']
        income_proj = projections['income']
        dividend_proj = projections['dividends']
        portfolio_proj = projections['portfolio_returns']
        retirement = projections['retirement_readiness']
        
        # Current state
        current_net_worth = net_worth_proj[0]['net_worth']
        
        # Future state (10 years or retirement)
        future_years = min(10, len(net_worth_proj) - 1)
        future_net_worth = net_worth_proj[future_years]['net_worth']
        future_income = income_proj[future_years]['gross_income']
        future_dividend = dividend_proj[future_years]['annual_dividend']
        
        return {
            'current_snapshot': {
                'net_worth': round(current_net_worth, 2),
                'annual_income': round(profile.annual_income, 2),
                'age': profile.age
            },
            'future_projection': {
                'years_ahead': future_years,
                'net_worth': round(future_net_worth, 2),
                'annual_income': round(future_income, 2),
                'annual_dividend': round(future_dividend, 2),
                'age': profile.age + future_years
            },
            'growth': {
                'net_worth_growth': round(((future_net_worth - current_net_worth) / abs(current_net_worth)) * 100 if current_net_worth != 0 else 0, 1),
                'income_growth': round(((future_income - profile.annual_income) / profile.annual_income) * 100, 1)
            },
            'retirement_outlook': retirement
        }
