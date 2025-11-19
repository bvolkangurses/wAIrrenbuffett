"""
Market Data Module - Fetches and analyzes stock market data
"""
import yfinance as yf
import pandas as pd
from typing import List, Dict, Optional
from datetime import datetime, timedelta


class MarketDataFetcher:
    """Fetches market data for stocks and analysis"""
    
    def __init__(self):
        self.cache = {}
    
    def get_stock_info(self, ticker: str) -> Dict:
        """Get detailed information about a stock"""
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # Extract relevant information
            stock_data = {
                'ticker': ticker,
                'name': info.get('longName', ticker),
                'sector': info.get('sector', 'Unknown'),
                'industry': info.get('industry', 'Unknown'),
                'current_price': info.get('currentPrice', info.get('regularMarketPrice', 0)),
                'market_cap': info.get('marketCap', 0),
                'pe_ratio': info.get('trailingPE', 0),
                'dividend_yield': info.get('dividendYield', 0),
                'beta': info.get('beta', 1.0),
                '52_week_high': info.get('fiftyTwoWeekHigh', 0),
                '52_week_low': info.get('fiftyTwoWeekLow', 0),
                'avg_volume': info.get('averageVolume', 0),
                'description': info.get('longBusinessSummary', '')[:200] + '...' if info.get('longBusinessSummary') else ''
            }
            
            return stock_data
        except Exception as e:
            print(f"Error fetching data for {ticker}: {e}")
            return None
    
    def get_historical_data(self, ticker: str, period: str = "1y") -> Optional[pd.DataFrame]:
        """Get historical price data for a stock"""
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period=period)
            return hist
        except Exception as e:
            print(f"Error fetching historical data for {ticker}: {e}")
            return None
    
    def calculate_returns(self, ticker: str, period: str = "1y") -> Dict:
        """Calculate various return metrics for a stock"""
        hist = self.get_historical_data(ticker, period)
        if hist is None or hist.empty:
            return None
        
        start_price = hist['Close'].iloc[0]
        end_price = hist['Close'].iloc[-1]
        total_return = ((end_price - start_price) / start_price) * 100
        
        # Calculate volatility (standard deviation of daily returns)
        daily_returns = hist['Close'].pct_change().dropna()
        volatility = daily_returns.std() * (252 ** 0.5) * 100  # Annualized
        
        return {
            'ticker': ticker,
            'period': period,
            'total_return': round(total_return, 2),
            'annualized_volatility': round(volatility, 2),
            'start_price': round(start_price, 2),
            'end_price': round(end_price, 2)
        }
    
    def get_sector_stocks(self, sector: str, limit: int = 10) -> List[str]:
        """Get popular stocks from a specific sector"""
        # Predefined lists of major stocks by sector
        sector_stocks = {
            'technology': ['AAPL', 'MSFT', 'GOOGL', 'META', 'NVDA', 'AVGO', 'CSCO', 'ADBE', 'CRM', 'INTC'],
            'tech': ['AAPL', 'MSFT', 'GOOGL', 'META', 'NVDA', 'AVGO', 'CSCO', 'ADBE', 'CRM', 'INTC'],
            'healthcare': ['JNJ', 'UNH', 'PFE', 'ABBV', 'MRK', 'TMO', 'ABT', 'DHR', 'LLY', 'BMY'],
            'finance': ['JPM', 'BAC', 'WFC', 'C', 'GS', 'MS', 'BLK', 'SCHW', 'AXP', 'USB'],
            'financial': ['JPM', 'BAC', 'WFC', 'C', 'GS', 'MS', 'BLK', 'SCHW', 'AXP', 'USB'],
            'energy': ['XOM', 'CVX', 'COP', 'SLB', 'EOG', 'MPC', 'PSX', 'VLO', 'OXY', 'HAL'],
            'consumer': ['AMZN', 'TSLA', 'WMT', 'HD', 'NKE', 'MCD', 'SBUX', 'TGT', 'LOW', 'DIS'],
            'industrial': ['BA', 'HON', 'UNP', 'CAT', 'GE', 'MMM', 'LMT', 'RTX', 'DE', 'UPS'],
            'utilities': ['NEE', 'DUK', 'SO', 'D', 'AEP', 'EXC', 'SRE', 'PEG', 'XEL', 'ED'],
            'real estate': ['AMT', 'PLD', 'CCI', 'EQIX', 'PSA', 'SPG', 'O', 'WELL', 'DLR', 'AVB'],
            'materials': ['LIN', 'APD', 'SHW', 'FCX', 'NEM', 'ECL', 'DD', 'DOW', 'NUE', 'VMC'],
            'telecommunications': ['T', 'VZ', 'TMUS', 'CMCSA', 'CHTR']
        }
        
        sector_lower = sector.lower()
        stocks = sector_stocks.get(sector_lower, [])
        return stocks[:limit]
    
    def get_dividend_stocks(self, limit: int = 20) -> List[str]:
        """Get a list of high dividend yield stocks"""
        # Well-known dividend aristocrats and high-yield stocks
        dividend_stocks = [
            'JNJ', 'PG', 'KO', 'PEP', 'MCD', 'WMT', 'XOM', 'CVX',
            'T', 'VZ', 'IBM', 'ABBV', 'MMM', 'CAT', 'TGT', 'O',
            'MO', 'SO', 'DUK', 'NEE'
        ]
        return dividend_stocks[:limit]
    
    def get_market_indices(self) -> Dict:
        """Get current values of major market indices"""
        indices = {
            'S&P 500': '^GSPC',
            'Dow Jones': '^DJI',
            'NASDAQ': '^IXIC'
        }
        
        results = {}
        for name, ticker in indices.items():
            try:
                index = yf.Ticker(ticker)
                info = index.info
                results[name] = {
                    'value': info.get('regularMarketPrice', 0),
                    'change': info.get('regularMarketChange', 0),
                    'change_percent': info.get('regularMarketChangePercent', 0)
                }
            except Exception as e:
                print(f"Error fetching {name}: {e}")
                results[name] = {'value': 0, 'change': 0, 'change_percent': 0}
        
        return results
