#!/usr/bin/env python3
"""
Basic tests for wAIrrenbuffett modules
"""
import sys
from user_profile import UserProfile
from ai_advisor import AIAdvisor
from financial_projections import FinancialProjector
from fallback_stocks import get_fallback_stock_data
from demo import get_demo_profile


def test_user_profile():
    """Test user profile creation"""
    print("Testing User Profile...")
    profile = UserProfile(
        age=35,
        location="Test City",
        annual_income=100000,
        current_savings=50000,
        monthly_expenses=3000,
        total_debt=20000,
        career_field="Engineering",
        years_to_retirement=30,
        expected_income_growth=3.0,
        marital_status="single",
        num_dependents=0,
        major_life_goals=["retirement", "travel"],
        risk_tolerance="moderate",
        investment_horizon=30,
        preferred_sectors=["technology"],
        other_notes="Test profile"
    )
    
    assert profile.age == 35
    assert profile.annual_income == 100000
    assert profile.risk_tolerance == "moderate"
    print("✓ User Profile test passed")
    return profile


def test_ai_advisor(profile):
    """Test AI advisor functionality"""
    print("\nTesting AI Advisor...")
    advisor = AIAdvisor(use_ollama=False)
    
    # Test profile analysis
    analysis = advisor.analyze_profile(profile)
    assert 'financial_health' in analysis
    assert 'recommended_allocation' in analysis
    assert 'investment_strategy' in analysis
    
    # Test allocation
    allocation = analysis['recommended_allocation']
    assert allocation['stocks'] + allocation['bonds'] == 100
    
    print("✓ AI Advisor test passed")
    return analysis


def test_stock_recommendations(profile):
    """Test stock recommendation generation"""
    print("\nTesting Stock Recommendations...")
    advisor = AIAdvisor(use_ollama=False)
    
    # Get fallback stock data
    stock_data = get_fallback_stock_data()
    assert len(stock_data) > 0
    
    # Generate recommendations
    recommendations = advisor.generate_stock_recommendations(
        profile, stock_data, num_picks=5
    )
    
    assert len(recommendations) <= 5
    assert len(recommendations) > 0
    
    # Check recommendation structure
    rec = recommendations[0]
    assert 'ticker' in rec
    assert 'name' in rec
    assert 'score' in rec
    assert 'rationale' in rec
    
    print(f"✓ Generated {len(recommendations)} recommendations")
    return recommendations


def test_financial_projections(profile, allocation):
    """Test financial projection calculations"""
    print("\nTesting Financial Projections...")
    projector = FinancialProjector()
    
    # Test net worth projection
    net_worth = projector.project_net_worth(profile, allocation, years=10)
    assert len(net_worth) == 11  # 0 to 10 years
    assert net_worth[0]['year'] == 0
    assert net_worth[10]['year'] == 10
    
    # Test income projection
    income = projector.project_income(profile, years=10)
    assert len(income) == 11
    assert income[10]['gross_income'] > income[0]['gross_income']
    
    # Test dividend projection
    dividends = projector.project_dividends(profile, [], years=10)
    assert len(dividends) == 11
    
    # Test portfolio returns
    returns = projector.project_portfolio_returns(profile, allocation, years=10)
    assert len(returns) == 11
    
    # Test retirement readiness
    retirement = projector.calculate_retirement_readiness(profile, net_worth)
    assert 'retirement_net_worth' in retirement
    assert 'retirement_goal' in retirement
    assert 'on_track' in retirement
    
    print("✓ Financial Projections test passed")
    return {
        'net_worth': net_worth,
        'income': income,
        'dividends': dividends,
        'portfolio_returns': returns,
        'retirement_readiness': retirement
    }


def test_demo_profiles():
    """Test all demo profiles"""
    print("\nTesting Demo Profiles...")
    scenarios = ['young', 'moderate', 'conservative', 'retirement']
    
    for scenario in scenarios:
        profile = get_demo_profile(scenario)
        assert profile is not None
        assert profile.age > 0
        assert profile.annual_income >= 0
        print(f"  ✓ {scenario.capitalize()} profile created")
    
    print("✓ All demo profiles test passed")


def test_comprehensive_workflow():
    """Test complete workflow"""
    print("\nTesting Comprehensive Workflow...")
    
    # Create profile
    profile = get_demo_profile("moderate")
    
    # Analyze with AI
    advisor = AIAdvisor(use_ollama=False)
    analysis = advisor.analyze_profile(profile)
    
    # Get stock data and recommendations
    stock_data = get_fallback_stock_data()
    recommendations = advisor.generate_stock_recommendations(
        profile, stock_data, num_picks=10
    )
    
    # Generate projections
    projector = FinancialProjector()
    allocation = analysis['recommended_allocation']
    projections = {
        'net_worth': projector.project_net_worth(profile, allocation),
        'income': projector.project_income(profile),
        'dividends': projector.project_dividends(profile, recommendations),
        'portfolio_returns': projector.project_portfolio_returns(profile, allocation)
    }
    
    # Generate summary
    projections['retirement_readiness'] = projector.calculate_retirement_readiness(
        profile, projections['net_worth']
    )
    summary = projector.generate_summary(profile, projections)
    
    assert 'current_snapshot' in summary
    assert 'future_projection' in summary
    assert 'growth' in summary
    
    print("✓ Comprehensive workflow test passed")


def main():
    """Run all tests"""
    print("=" * 60)
    print("  wAIrrenbuffett Basic Tests")
    print("=" * 60)
    
    try:
        profile = test_user_profile()
        analysis = test_ai_advisor(profile)
        recommendations = test_stock_recommendations(profile)
        projections = test_financial_projections(
            profile, 
            analysis['recommended_allocation']
        )
        test_demo_profiles()
        test_comprehensive_workflow()
        
        print("\n" + "=" * 60)
        print("  ✓ ALL TESTS PASSED")
        print("=" * 60)
        return 0
        
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
