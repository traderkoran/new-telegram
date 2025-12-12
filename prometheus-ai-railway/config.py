import os
from typing import Dict, List

class Config:
    # API Keys (Set via environment variables)
    TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN', '')
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '')
    
    # Bot settings
    BOT_USERNAME = "PrometheusUltraBot"
    ADMIN_IDS = []  # Add admin Telegram IDs if needed
    
    # Analysis settings
    DEFAULT_TIMEFRAMES = ['1h', '4h', '1d', '1w']
    MAX_ASSETS_PER_REQUEST = 5
    
    # Data settings
    CACHE_DURATION = 300  # 5 minutes
    REQUEST_TIMEOUT = 30
    
    # Supported assets
    CRYPTO_SYMBOLS = [
        'BTC', 'ETH', 'BNB', 'XRP', 'ADA', 'SOL', 'DOGE', 'DOT', 
        'MATIC', 'AVAX', 'LINK', 'LTC', 'UNI', 'ATOM'
    ]
    
    STOCK_SYMBOLS = [
        'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NVDA',
        'JPM', 'V', 'JNJ', 'WMT', 'PG', 'MA', 'DIS'
    ]
    
    FOREX_PAIRS = [
        'EURUSD', 'GBPUSD', 'USDJPY', 'AUDUSD', 'USDCAD',
        'USDCHF', 'NZDUSD', 'EURGBP', 'EURJPY'
    ]
    
    # Risk management
    MAX_RISK_PER_TRADE = 0.02  # 2%
    MIN_RISK_REWARD_RATIO = 2.0
    
    # Gemini AI settings
    GEMINI_MODEL = "gemini-1.5-flash"
    MAX_TOKENS = 4000
    TEMPERATURE = 0.7

config = Config()
