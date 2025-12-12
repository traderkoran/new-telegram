"""
Formatting utilities for analysis reports
"""

from typing import Dict, Any, List
from datetime import datetime

def format_analysis_report(analysis_result: Dict[str, Any]) -> str:
    """
    Format analysis result into a readable Telegram message
    
    Args:
        analysis_result: Comprehensive analysis result dictionary
        
    Returns:
        Formatted message string
    """
    
    symbol = analysis_result.get("symbol", "UNKNOWN")
    signal = analysis_result.get("final_signal", {}).get("decision", "HOLD")
    confidence = analysis_result.get("final_signal", {}).get("confidence_score", 0)
    risk_level = analysis_result.get("final_signal", {}).get("risk_level", "MEDIUM")
    
    # Get emoji for signal
    signal_emoji = {
        "STRONG_BUY": "🟢",
        "BUY": "✅",
        "HOLD": "🟡",
        "SELL": "🔴",
        "STRONG_SELL": "🛑"
    }.get(signal, "⚪")
    
    # Get emoji for risk
    risk_emoji = {
        "VERY_HIGH": "🔴🔴🔴",
        "HIGH": "🔴🔴",
        "MEDIUM": "🟡🟡",
        "LOW": "🟢🟢",
        "VERY_LOW": "🟢"
    }.get(risk_level, "⚪")
    
    current_price = analysis_result.get("current_price", 0)
    price_change = analysis_result.get("price_change_24h", 0)
    
    # Format price change with color
    if price_change > 0:
        price_change_str = f"📈 +{price_change:.2f}%"
    elif price_change < 0:
        price_change_str = f"📉 {price_change:.2f}%"
    else:
        price_change_str = f"➡️ {price_change:.2f}%"
    
    # Start building the message
    message = f"""
{symbol_emoji(symbol)} *{symbol} - TAM ANALİZ RAPORU*
{signal_emoji} *KARAR: {signal}*
⏰ {datetime.now().strftime("%d.%m.%Y %H:%M")}

🎯 *YÖNETİCİ ÖZETİ*
