# wAIrrenbuffett 📈

An AI-assisted financial planner and investor that gives you personalized stock picks and financial projections.

## Overview

wAIrrenbuffett is a comprehensive financial planning tool that uses AI and real-time market data to provide:

- **Personalized Stock Recommendations** - Get stock picks tailored to your profile, risk tolerance, and sector preferences
- **Net Worth Projections** - See how your wealth will grow over time based on income, expenses, and investment returns
- **Income Forecasting** - Project your income growth considering career trajectory and inflation
- **Dividend Income Predictions** - Estimate future passive income from dividend-paying stocks
- **Retirement Readiness Analysis** - Understand if you're on track to meet your retirement goals
- **Comprehensive Financial Health Assessment** - Get insights into savings rate, debt-to-income ratio, and more

## Features

### 🤖 AI-Powered Analysis
- Uses open-source foundation models (with Ollama support) to analyze your financial profile
- Rule-based intelligent recommendations when AI models aren't available
- Personalized investment strategies based on your unique situation

### 📊 Real-Time Market Data
- Fetches live stock prices, dividend yields, P/E ratios, and more using yfinance
- Analyzes stocks across multiple sectors and industries
- Includes major indices tracking (S&P 500, Dow Jones, NASDAQ)

### 💰 Comprehensive Projections
- **Net Worth**: Year-by-year projections considering income growth, expenses, and investment returns
- **Income**: Future income estimates with career growth and inflation adjustments
- **Dividends**: Projected passive income from dividend stocks
- **Portfolio Returns**: Expected, best-case, worst-case, and conservative scenarios
- **Retirement Planning**: 4% rule analysis and retirement goal tracking

### 🎯 Personalized Recommendations
- Stock scoring based on your risk tolerance, preferred sectors, and investment horizon
- Asset allocation suggestions (stocks vs. bonds breakdown)
- Clear rationale for each recommendation
- Considers valuation metrics, volatility, and dividend yields

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/bvolkangurses/wAIrrenbuffett.git
cd wAIrrenbuffett
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. (Optional) For AI-powered insights, install Ollama:
```bash
# Follow instructions at https://ollama.ai
# Then pull a model:
ollama pull llama2
```

## Usage

### Interactive Mode

Run the main application:
```bash
python main.py
```

The application will guide you through a series of questions about:
- Your age, location, and career field
- Current financial situation (income, savings, expenses, debt)
- Career aspirations and retirement timeline
- Family situation and major life goals
- Investment preferences and risk tolerance

After collecting your information, wAIrrenbuffett will:
1. Analyze your financial health
2. Recommend an investment strategy and asset allocation
3. Generate personalized stock picks
4. Project your financial future across multiple dimensions
5. Assess your retirement readiness

### Example Session

```
Welcome to wAIrrenbuffett - AI Financial Planner

--- Personal Information ---
What is your age? 35
What is your location (city, country)? San Francisco, USA

--- Current Financial Situation ---
What is your annual income (before taxes)? $120000
How much do you currently have in savings/investments? $85000
What are your average monthly expenses? $4500
What is your total debt (mortgage, loans, credit cards)? $15000

... (continues with more questions)
```

## Project Structure

```
wAIrrenbuffett/
├── main.py                    # Main application entry point
├── user_profile.py            # User profile data collection and management
├── market_data.py             # Stock market data fetching and analysis
├── ai_advisor.py              # AI-powered financial analysis and recommendations
├── financial_projections.py   # Financial projection calculations
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## How It Works

### 1. Profile Collection
The system collects comprehensive information about your:
- Demographics and career
- Current financial situation
- Goals and aspirations
- Risk tolerance and preferences

### 2. Financial Analysis
Calculates key metrics:
- Savings rate
- Debt-to-income ratio
- Emergency fund adequacy
- Risk assessment

### 3. AI Recommendations
Generates personalized advice:
- Asset allocation tailored to your age and risk tolerance
- Investment strategy aligned with your goals
- Stock picks scored based on your preferences

### 4. Market Data Integration
Fetches real-time data:
- Stock prices and fundamental metrics
- Dividend yields and P/E ratios
- Sector and industry information
- Market volatility indicators

### 5. Projection Engine
Calculates future scenarios:
- Net worth growth with investment returns
- Income progression with raises and inflation
- Dividend income accumulation
- Retirement funding analysis

## Investment Philosophy

wAIrrenbuffett follows sound financial principles:

- **Diversification**: Recommends balanced portfolios across sectors and asset classes
- **Risk Management**: Adjusts recommendations based on your risk tolerance and time horizon
- **Long-term Focus**: Emphasizes sustained growth over market timing
- **Value Consideration**: Evaluates stocks based on fundamentals, not just momentum
- **Income Generation**: Incorporates dividend-paying stocks for passive income
- **Retirement Planning**: Uses the proven 4% safe withdrawal rule

## Asset Allocation Strategy

The recommended allocation follows the principle: **110 - Age = Stock %**

Adjusted for risk tolerance:
- **Conservative**: -15% from base (more bonds)
- **Moderate**: Base allocation
- **Aggressive**: +15% from base (more stocks)

Example for a 35-year-old moderate investor:
- Base stock allocation: 75% (110 - 35)
- Bonds: 25%
- Stock breakdown: Large-cap (60%), Mid-cap (25%), Small-cap (10%), International (5%)

## Stock Scoring System

Stocks are scored (0-100) based on:
- Sector match with your preferences: +15 points
- Risk tolerance alignment (beta): ±10 points
- Dividend yield (for conservative investors): +15 points
- Valuation (P/E ratio): +10 points
- Market cap size match: +5-10 points

## Disclaimers

⚠️ **Important**: 
- This tool is for **educational and informational purposes only**
- Not a substitute for professional financial advice
- Past performance does not guarantee future results
- Stock market investments carry risk, including potential loss of principal
- Always consult with a qualified financial advisor before making investment decisions
- The AI recommendations are based on historical data and general principles
- Individual circumstances may require different strategies

## Dependencies

- **yfinance**: Real-time stock market data
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computations
- **requests**: HTTP library for API calls
- **python-dotenv**: Environment variable management
- **ollama**: (Optional) Local LLM integration

## Future Enhancements

Potential features for future versions:
- Interactive web interface
- Portfolio tracking and rebalancing alerts
- Tax optimization strategies
- Estate planning considerations
- Integration with brokerage APIs
- Machine learning-based return predictions
- Monte Carlo simulations for risk analysis
- Backtesting of recommended strategies

## Contributing

Contributions are welcome! Please feel free to submit issues, fork the repository, and create pull requests.

## License

This project is open source and available for educational purposes.

## Acknowledgments

- Market data provided by Yahoo Finance (via yfinance)
- Inspired by the investment philosophy of Warren Buffett
- Built with modern Python best practices

---

**Made with 📊 and 🤖 for better financial planning**
