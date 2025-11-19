"""
User Profile Module - Collects and manages user financial profile information
"""
from dataclasses import dataclass
from typing import Optional, List
import json


@dataclass
class UserProfile:
    """User financial profile data"""
    # Personal Information
    age: int
    location: str
    
    # Financial Situation
    annual_income: float
    current_savings: float
    monthly_expenses: float
    total_debt: float
    
    # Career & Goals
    career_field: str
    years_to_retirement: int
    expected_income_growth: float  # Annual percentage
    
    # Family & Dependents
    marital_status: str
    num_dependents: int
    major_life_goals: List[str]
    
    # Investment Profile
    risk_tolerance: str  # conservative, moderate, aggressive
    investment_horizon: int  # years
    preferred_sectors: List[str]
    
    # Additional Context
    other_notes: str = ""
    
    def to_dict(self):
        """Convert profile to dictionary"""
        return {
            'age': self.age,
            'location': self.location,
            'annual_income': self.annual_income,
            'current_savings': self.current_savings,
            'monthly_expenses': self.monthly_expenses,
            'total_debt': self.total_debt,
            'career_field': self.career_field,
            'years_to_retirement': self.years_to_retirement,
            'expected_income_growth': self.expected_income_growth,
            'marital_status': self.marital_status,
            'num_dependents': self.num_dependents,
            'major_life_goals': self.major_life_goals,
            'risk_tolerance': self.risk_tolerance,
            'investment_horizon': self.investment_horizon,
            'preferred_sectors': self.preferred_sectors,
            'other_notes': self.other_notes
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create profile from dictionary"""
        return cls(**data)
    
    def save(self, filepath: str):
        """Save profile to JSON file"""
        with open(filepath, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)
    
    @classmethod
    def load(cls, filepath: str):
        """Load profile from JSON file"""
        with open(filepath, 'r') as f:
            data = json.load(f)
        return cls.from_dict(data)


def collect_user_profile() -> UserProfile:
    """Interactive function to collect user profile information"""
    print("=" * 60)
    print("Welcome to wAIrrenbuffett - AI Financial Planner")
    print("=" * 60)
    print("\nLet's get to know you and your financial goals.\n")
    
    # Personal Information
    print("--- Personal Information ---")
    age = int(input("What is your age? "))
    location = input("What is your location (city, country)? ")
    
    # Financial Situation
    print("\n--- Current Financial Situation ---")
    annual_income = float(input("What is your annual income (before taxes)? $"))
    current_savings = float(input("How much do you currently have in savings/investments? $"))
    monthly_expenses = float(input("What are your average monthly expenses? $"))
    total_debt = float(input("What is your total debt (mortgage, loans, credit cards)? $"))
    
    # Career & Goals
    print("\n--- Career Information ---")
    career_field = input("What is your career field? ")
    years_to_retirement = int(input("How many years until you plan to retire? "))
    expected_income_growth = float(input("Expected annual income growth rate (as %, e.g., 3.5)? "))
    
    # Family & Dependents
    print("\n--- Family & Life Goals ---")
    marital_status = input("Marital status (single/married/divorced/widowed)? ")
    num_dependents = int(input("Number of dependents (children, etc.)? "))
    
    print("\nList your major life goals (one per line, empty line to finish):")
    major_life_goals = []
    while True:
        goal = input("  Goal: ")
        if not goal:
            break
        major_life_goals.append(goal)
    
    # Investment Profile
    print("\n--- Investment Profile ---")
    print("Risk Tolerance Options: conservative, moderate, aggressive")
    risk_tolerance = input("What is your risk tolerance? ").lower()
    investment_horizon = int(input("Investment time horizon in years? "))
    
    print("\nList preferred sectors (e.g., tech, healthcare, energy) (one per line, empty to finish):")
    preferred_sectors = []
    while True:
        sector = input("  Sector: ")
        if not sector:
            break
        preferred_sectors.append(sector)
    
    # Additional Context
    print("\n--- Additional Information ---")
    other_notes = input("Any other relevant information? ")
    
    profile = UserProfile(
        age=age,
        location=location,
        annual_income=annual_income,
        current_savings=current_savings,
        monthly_expenses=monthly_expenses,
        total_debt=total_debt,
        career_field=career_field,
        years_to_retirement=years_to_retirement,
        expected_income_growth=expected_income_growth,
        marital_status=marital_status,
        num_dependents=num_dependents,
        major_life_goals=major_life_goals,
        risk_tolerance=risk_tolerance,
        investment_horizon=investment_horizon,
        preferred_sectors=preferred_sectors,
        other_notes=other_notes
    )
    
    print("\n" + "=" * 60)
    print("Profile collected successfully!")
    print("=" * 60 + "\n")
    
    return profile
