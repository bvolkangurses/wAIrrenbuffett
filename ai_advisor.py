"""
AI Advisor Module - Uses LLM to analyze profiles and make recommendations
"""
from typing import List, Dict, Optional
from user_profile import UserProfile
import json


class AIAdvisor:
    """AI-powered financial advisor using LLM"""
    
    def __init__(self, use_ollama: bool = False):
        """
        Initialize AI Advisor
        
        Args:
            use_ollama: If True, uses Ollama for local LLM. Otherwise uses rule-based system.
        """
        self.use_ollama = use_ollama
        self.ollama_client = None
        
        if use_ollama:
            try:
                import ollama
                self.ollama_client = ollama
            except ImportError:
                print("Warning: Ollama not available. Falling back to rule-based system.")
                self.use_ollama = False
    
    def analyze_profile(self, profile: UserProfile) -> Dict:
        """Analyze user profile and generate insights"""
        
        # Calculate key metrics
        monthly_income = profile.annual_income / 12
        savings_rate = ((monthly_income - profile.monthly_expenses) / monthly_income) * 100
        debt_to_income_ratio = (profile.total_debt / profile.annual_income) * 100
        years_to_debt_free = profile.total_debt / ((monthly_income - profile.monthly_expenses) * 12) if monthly_income > profile.monthly_expenses else float('inf')
        
        # Determine investment allocation based on risk tolerance and age
        allocation = self._determine_allocation(profile)
        
        analysis = {
            'financial_health': {
                'savings_rate': round(savings_rate, 2),
                'debt_to_income_ratio': round(debt_to_income_ratio, 2),
                'years_to_debt_free': round(years_to_debt_free, 2) if years_to_debt_free != float('inf') else 'N/A',
                'emergency_fund_months': round(profile.current_savings / profile.monthly_expenses, 1),
            },
            'recommended_allocation': allocation,
            'investment_strategy': self._determine_strategy(profile),
            'risk_assessment': self._assess_risk(profile)
        }
        
        if self.use_ollama and self.ollama_client:
            # Enhance with LLM analysis
            analysis['ai_insights'] = self._get_llm_insights(profile, analysis)
        
        return analysis
    
    def _determine_allocation(self, profile: UserProfile) -> Dict:
        """Determine asset allocation based on profile"""
        # Rule of thumb: 110 - age = stock percentage
        base_stock_percentage = 110 - profile.age
        
        # Adjust based on risk tolerance
        risk_adjustments = {
            'conservative': -15,
            'moderate': 0,
            'aggressive': 15
        }
        
        adjustment = risk_adjustments.get(profile.risk_tolerance, 0)
        stock_percentage = max(30, min(90, base_stock_percentage + adjustment))
        bond_percentage = 100 - stock_percentage
        
        # Further breakdown of stock allocation
        large_cap = stock_percentage * 0.60
        mid_cap = stock_percentage * 0.25
        small_cap = stock_percentage * 0.10
        international = stock_percentage * 0.05
        
        return {
            'stocks': round(stock_percentage, 1),
            'bonds': round(bond_percentage, 1),
            'breakdown': {
                'large_cap': round(large_cap, 1),
                'mid_cap': round(mid_cap, 1),
                'small_cap': round(small_cap, 1),
                'international': round(international, 1),
                'bonds': round(bond_percentage, 1)
            }
        }
    
    def _determine_strategy(self, profile: UserProfile) -> str:
        """Determine overall investment strategy"""
        if profile.years_to_retirement <= 5:
            return "Capital Preservation - Focus on stable dividend stocks and bonds"
        elif profile.years_to_retirement <= 15:
            return "Balanced Growth - Mix of growth and dividend stocks with some bonds"
        else:
            if profile.risk_tolerance == 'aggressive':
                return "Aggressive Growth - Focus on high-growth stocks and emerging sectors"
            elif profile.risk_tolerance == 'conservative':
                return "Conservative Growth - Blue-chip dividend stocks and bonds"
            else:
                return "Moderate Growth - Diversified portfolio with growth and value stocks"
    
    def _assess_risk(self, profile: UserProfile) -> str:
        """Assess overall risk profile"""
        risk_factors = []
        
        # Income stability
        if profile.annual_income < 50000:
            risk_factors.append("Lower income requires more conservative approach")
        
        # Debt level
        debt_to_income = (profile.total_debt / profile.annual_income) * 100
        if debt_to_income > 40:
            risk_factors.append("High debt-to-income ratio")
        
        # Emergency fund
        emergency_months = profile.current_savings / profile.monthly_expenses
        if emergency_months < 3:
            risk_factors.append("Insufficient emergency fund")
        
        # Dependents
        if profile.num_dependents > 0:
            risk_factors.append("Financial responsibility for dependents")
        
        # Time horizon
        if profile.years_to_retirement < 10:
            risk_factors.append("Short time horizon for retirement")
        
        if len(risk_factors) >= 3:
            return "High Risk - Consider conservative investments and building emergency fund"
        elif len(risk_factors) >= 1:
            return "Moderate Risk - Balance growth with stability"
        else:
            return "Low Risk - Good position for long-term growth investing"
    
    def generate_stock_recommendations(self, profile: UserProfile, 
                                      stock_data: List[Dict],
                                      num_picks: int = 10) -> List[Dict]:
        """Generate personalized stock recommendations"""
        recommendations = []
        
        # Score stocks based on profile
        for stock in stock_data:
            if stock is None:
                continue
            
            score = self._score_stock(stock, profile)
            
            if score > 0:
                recommendations.append({
                    'ticker': stock['ticker'],
                    'name': stock['name'],
                    'sector': stock['sector'],
                    'current_price': stock['current_price'],
                    'dividend_yield': stock['dividend_yield'],
                    'pe_ratio': stock['pe_ratio'],
                    'score': score,
                    'rationale': self._generate_rationale(stock, profile)
                })
        
        # Sort by score and return top picks
        recommendations.sort(key=lambda x: x['score'], reverse=True)
        return recommendations[:num_picks]
    
    def _score_stock(self, stock: Dict, profile: UserProfile) -> float:
        """Score a stock based on user profile"""
        score = 50.0  # Base score
        
        # Sector preference
        if stock['sector'].lower() in [s.lower() for s in profile.preferred_sectors]:
            score += 15
        
        # Risk tolerance adjustments
        beta = stock.get('beta', 1.0)
        if profile.risk_tolerance == 'conservative':
            if beta < 0.8:
                score += 10
            elif beta > 1.2:
                score -= 10
            # Prefer dividend stocks
            if stock['dividend_yield'] and stock['dividend_yield'] > 0.02:
                score += 15
        elif profile.risk_tolerance == 'aggressive':
            if beta > 1.2:
                score += 10
            # Less emphasis on dividends
            score += 5
        else:  # moderate
            if 0.8 <= beta <= 1.2:
                score += 10
            if stock['dividend_yield'] and stock['dividend_yield'] > 0.015:
                score += 10
        
        # P/E ratio (value consideration)
        pe_ratio = stock.get('pe_ratio', 0)
        if pe_ratio and 10 <= pe_ratio <= 25:
            score += 10
        elif pe_ratio and pe_ratio > 40:
            score -= 5
        
        # Market cap (stability consideration)
        market_cap = stock.get('market_cap', 0)
        if market_cap > 100_000_000_000:  # Large cap
            if profile.risk_tolerance == 'conservative':
                score += 10
        elif market_cap < 10_000_000_000:  # Small cap
            if profile.risk_tolerance == 'aggressive':
                score += 5
        
        return round(score, 2)
    
    def _generate_rationale(self, stock: Dict, profile: UserProfile) -> str:
        """Generate explanation for stock recommendation"""
        reasons = []
        
        if stock['sector'].lower() in [s.lower() for s in profile.preferred_sectors]:
            reasons.append(f"Matches your interest in {stock['sector']}")
        
        if stock['dividend_yield'] and stock['dividend_yield'] > 0.03:
            reasons.append(f"Strong dividend yield of {stock['dividend_yield']*100:.2f}%")
        
        if stock.get('beta', 1.0) < 0.9 and profile.risk_tolerance == 'conservative':
            reasons.append("Lower volatility matches your risk tolerance")
        
        if stock.get('beta', 1.0) > 1.1 and profile.risk_tolerance == 'aggressive':
            reasons.append("Higher growth potential for aggressive strategy")
        
        pe_ratio = stock.get('pe_ratio', 0)
        if pe_ratio and 10 <= pe_ratio <= 20:
            reasons.append("Reasonable valuation")
        
        if not reasons:
            reasons.append("Solid fundamentals for diversified portfolio")
        
        return "; ".join(reasons)
    
    def _get_llm_insights(self, profile: UserProfile, analysis: Dict) -> str:
        """Get additional insights from LLM (if available)"""
        if not self.ollama_client:
            return ""
        
        try:
            prompt = f"""Analyze this financial profile and provide personalized investment advice:

Age: {profile.age}
Income: ${profile.annual_income:,.0f}
Savings: ${profile.current_savings:,.0f}
Risk Tolerance: {profile.risk_tolerance}
Years to Retirement: {profile.years_to_retirement}
Goals: {', '.join(profile.major_life_goals)}

Current Analysis:
- Savings Rate: {analysis['financial_health']['savings_rate']:.1f}%
- Investment Strategy: {analysis['investment_strategy']}

Provide 2-3 key personalized insights and recommendations."""

            response = self.ollama_client.generate(
                model='llama2',
                prompt=prompt
            )
            
            return response.get('response', '')
        except Exception as e:
            print(f"LLM analysis error: {e}")
            return ""
