"""
Demo module - Provides sample profiles for testing
"""
from user_profile import UserProfile


def get_demo_profile(scenario: str = "moderate") -> UserProfile:
    """
    Get a demo user profile for testing
    
    Args:
        scenario: Type of demo profile (young, moderate, conservative, retirement)
    """
    
    if scenario == "young":
        # Young professional, aggressive investor
        return UserProfile(
            age=28,
            location="Austin, TX",
            annual_income=85000,
            current_savings=25000,
            monthly_expenses=3200,
            total_debt=35000,
            career_field="Software Engineering",
            years_to_retirement=37,
            expected_income_growth=5.0,
            marital_status="single",
            num_dependents=0,
            major_life_goals=[
                "Buy a house in 5 years",
                "Build wealth for early retirement",
                "Travel internationally"
            ],
            risk_tolerance="aggressive",
            investment_horizon=35,
            preferred_sectors=["technology", "healthcare", "finance"],
            other_notes="Tech-savvy, interested in growth stocks"
        )
    
    elif scenario == "moderate":
        # Mid-career professional with family
        return UserProfile(
            age=38,
            location="Chicago, IL",
            annual_income=125000,
            current_savings=180000,
            monthly_expenses=5500,
            total_debt=280000,
            career_field="Marketing Manager",
            years_to_retirement=27,
            expected_income_growth=3.5,
            marital_status="married",
            num_dependents=2,
            major_life_goals=[
                "Save for children's college education",
                "Pay off mortgage early",
                "Comfortable retirement",
                "Family vacations"
            ],
            risk_tolerance="moderate",
            investment_horizon=25,
            preferred_sectors=["consumer", "healthcare", "technology"],
            other_notes="Family-oriented, balanced approach to investing"
        )
    
    elif scenario == "conservative":
        # Established professional nearing retirement
        return UserProfile(
            age=52,
            location="Denver, CO",
            annual_income=145000,
            current_savings=525000,
            monthly_expenses=6800,
            total_debt=85000,
            career_field="Financial Analyst",
            years_to_retirement=13,
            expected_income_growth=2.5,
            marital_status="married",
            num_dependents=0,
            major_life_goals=[
                "Retire comfortably at 65",
                "Generate passive income",
                "Travel during retirement",
                "Leave inheritance for children"
            ],
            risk_tolerance="conservative",
            investment_horizon=13,
            preferred_sectors=["utilities", "consumer", "healthcare"],
            other_notes="Focus on capital preservation and income generation"
        )
    
    elif scenario == "retirement":
        # Recently retired individual
        return UserProfile(
            age=67,
            location="Phoenix, AZ",
            annual_income=45000,
            current_savings=850000,
            monthly_expenses=4200,
            total_debt=0,
            career_field="Retired Teacher",
            years_to_retirement=0,
            expected_income_growth=0.0,
            marital_status="widowed",
            num_dependents=0,
            major_life_goals=[
                "Maintain standard of living",
                "Healthcare expenses",
                "Stay financially independent",
                "Support grandchildren"
            ],
            risk_tolerance="conservative",
            investment_horizon=5,
            preferred_sectors=["utilities", "consumer", "healthcare"],
            other_notes="Retired, focus on income and preservation"
        )
    
    else:
        # Default to moderate scenario
        return get_demo_profile("moderate")


def print_demo_info(scenario: str):
    """Print information about the demo scenario"""
    descriptions = {
        "young": "Young Professional - Aggressive growth strategy, long time horizon",
        "moderate": "Mid-Career Family - Balanced approach with dependents",
        "conservative": "Pre-Retirement - Focus on stability and income",
        "retirement": "Recently Retired - Capital preservation and income"
    }
    
    print("\n" + "=" * 70)
    print(f"  DEMO MODE: {scenario.upper()}")
    print(f"  {descriptions.get(scenario, 'Standard demo profile')}")
    print("=" * 70 + "\n")
