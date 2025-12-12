"""
Universal data fetcher for multiple asset classes
"""

import yfinance as yf
import pandas as pd
import numpy as np
from typing import Optional, Dict, Any
import asyncio
import aiohttp
from datetime import datetime, timedelta
import ccxt
from cachetools import TTLCache

class UniversalDataClient:
    def __init__(self):
        self.cache = TTLCache(maxsize=100, ttl=300)  # 5 minutes cache
        self.ccxt_exchange = ccxt.binance()
        
    async def fetch_data(self, symbol: str, period: str = "7d", interval: str = "1h") -> Optional[pd.DataFrame]:
        """
        Fetch data for any symbol
        
        Args:
            symbol: Asset symbol (BTC, AAPL, EURUSD, etc.)
            period: Time period (1d, 7d, 1mo, 3mo, 6mo, 1y, 2y, 5y)
            interval: Data interval (1m, 5m, 15m, 30m, 1h, 1d, 1wk, 1mo)
            
        Returns:
            pandas DataFrame with OHLCV data
        """
        
        cache_key = f"{symbol}_{period}_{interval}"
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        try:
            # Determine asset type and fetch accordingly
            if self._is_crypto(symbol):
                data = await self._fetch_crypto_data(symbol, period, interval)
            elif self._is_forex(symbol):
                data = await self._fetch_forex_data(symbol, period, interval)
            elif self._is_commodity(symbol):
                data = await self._fetch_commodity_data(symbol, period, interval)
            else:
                data = await self._fetch_stock_data(symbol, period, interval)
            
            if data is not None and not data.empty:
                self.cache[cache_key] = data
            
            return data
            
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")
            return None
    
    def _is_crypto(self, symbol: str) -> bool:
        """Check if symbol is cryptocurrency"""
        crypto_symbols = ["BTC", "ETH", "BNB", "XRP", "ADA", "SOL", "DOGE", 
                         "DOT", "MATIC", "AVAX", "LINK", "LTC", "UNI", "ATOM"]
        return symbol.upper() in crypto_symbols or symbol.endswith('USD') or symbol.endswith('USDT')
    
    def _is_forex(self, symbol: str) -> bool:
        """Check if symbol is forex pair"""
        forex_pairs = ["EURUSD", "GBPUSD", "USDJPY", "AUDUSD", "USDCAD",
                      "USDCHF", "NZDUSD", "EURGBP", "EURJPY", "GBPJPY"]
        return symbol.upper() in forex_pairs
    
    def _is_commodity(self, symbol: str) -> bool:
        """Check if symbol is commodity"""
        commodities = ["GOLD", "XAUUSD", "SILVER", "XAGUSD", "OIL", "CL", "BRENT"]
        return symbol.upper() in commodities
    
    async def _fetch_stock_data(self, symbol: str, period: str, interval: str) -> Optional[pd.DataFrame]:
        """Fetch stock data using yfinance"""
        try:
            ticker = yf.Ticker(symbol)
            df = ticker.history(period=period, interval=interval)
            
            if df.empty:
                # Try with .NS for Indian stocks
                ticker = yf.Ticker(f"{symbol}.NS")
                df = ticker.history(period=period, interval=interval)
            
            return self._clean_dataframe(df)
            
        except Exception as e:
            print(f"Error fetching stock data for {symbol}: {e}")
            return None
    
    async def _fetch_crypto_data(self, symbol: str, period: str, interval: str) -> Optional[pd.DataFrame]:
        """Fetch cryptocurrency data"""
        try:
            # Map interval for CCXT
            interval_map = {
                "1m": "1m", "5m": "5m", "15m": "15m", "30m": "30m",
                "1h": "1h", "1d": "1d", "1wk": "1w", "1mo": "1M"
            }
            
            ccxt_interval = interval_map.get(interval, "1h")
            
            # Map symbol for CCXT
            if symbol.endswith('USD') or symbol.endswith('USDT'):
                ccxt_symbol = f"{symbol}/USDT"
            else:
                ccxt_symbol = f"{symbol}/USDT"
            
            # Calculate since parameter based on period
            since_map = {
                "1d": int((datetime.now() - timedelta(days=1)).timestamp() * 1000),
                "7d": int((datetime.now() - timedelta(days=7)).timestamp() * 1000),
                "1mo": int((datetime.now() - timedelta(days=30)).timestamp() * 1000),
                "3mo": int((datetime.now() - timedelta(days=90)).timestamp() * 1000),
                "6mo": int((datetime.now() - timedelta(days=180)).timestamp() * 1000),
                "1y": int((datetime.now() - timedelta(days=365)).timestamp() * 1000),
            }
            
            since = since_map.get(period, since_map["7d"])
            
            # Fetch OHLCV data
            ohlcv = self.ccxt_exchange.fetch_ohlcv(
                ccxt_symbol, 
                timeframe=ccxt_interval,
                since=since,
                limit=1000
            )
            
            df = pd.DataFrame(
                ohlcv, 
                columns=['timestamp', 'Open', 'High', 'Low', 'Close', 'Volume']
            )
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df.set_index('timestamp', inplace=True)
            
            return self._clean_dataframe(df)
            
        except Exception as e:
            print(f"Error fetching crypto data for {symbol}: {e}")
            # Fallback to yfinance for major cryptos
            try:
                ticker = yf.Ticker(f"{symbol}-USD")
                df = ticker.history(period=period, interval=interval)
                return self._clean_dataframe(df)
            except:
                return None
    
    async def _fetch_forex_data(self, symbol: str, period: str, interval: str) -> Optional[pd.DataFrame]:
        """Fetch forex data using yfinance"""
        try:
            # Forex symbols in yfinance format
            if 'USD' in symbol:
                yf_symbol = symbol.replace('USD', '=X')
            else:
                yf_symbol = f"{symbol}=X"
            
            ticker = yf.Ticker(yf_symbol)
            df = ticker.history(period=period, interval=interval)
            
            return self._clean_dataframe(df)
            
        except Exception as e:
            print(f"Error fetching forex data for {symbol}: {e}")
            return None
    
    async def _fetch_commodity_data(self, symbol: str, period: str, interval: str) -> Optional[pd.DataFrame]:
        """Fetch commodity data"""
        try:
            # Map commodity symbols to yfinance symbols
            symbol_map = {
                "GOLD": "GC=F", "XAUUSD": "GC=F",
                "SILVER": "SI=F", "XAGUSD": "SI=F",
                "OIL": "CL=F", "CL": "CL=F", "BRENT": "BZ=F"
            }
            
            yf_symbol = symbol_map.get(symbol.upper(), symbol)
            ticker = yf.Ticker(yf_symbol)
            df = ticker.history(period=period, interval=interval)
            
            return self._clean_dataframe(df)
            
        except Exception as e:
            print(f"Error fetching commodity data for {symbol}: {e}")
            return None
    
    def _clean_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and prepare dataframe"""
        if df.empty:
            return df
        
        # Ensure we have required columns
        required_columns = ['Open', 'High', 'Low', 'Close']
        for col in required_columns:
            if col not in df.columns:
                df[col] = 0
        
        # Add Volume if missing
        if 'Volume' not in df.columns:
            df['Volume'] = 0
        
        # Remove any rows with NaN values in OHLC
        df = df.dropna(subset=required_columns)
        
        # Ensure numeric types
        for col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        return df
    
    async def get_current_price(self, symbol: str) -> Optional[float]:
        """Get current price for a symbol"""
        try:
            data = await self.fetch_data(symbol, period="1d", interval="1h")
            if data is not None and not data.empty:
                return float(data['Close'].iloc[-1])
        except:
            pass
        return None
    
    async def get_price_change_24h(self, symbol: str) -> Optional[float]:
        """Get 24-hour price change percentage"""
        try:
            data = await self.fetch_data(symbol, period="2d", interval="1h")
            if data is not None and len(data) >= 24:
                current = data['Close'].iloc[-1]
                prev_24h = data['Close'].iloc[-24]
                return ((current - prev_24h) / prev_24h) * 100
        except:
            pass
        return None
