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

📊 *TEKNİK ANALİZ ÖZETİ*
"""
    
    # Add technical summary
    technical = analysis_result.get("technical_indicators", {})
    momentum = technical.get("momentum", {})
    trend = technical.get("trend", {})
    
    # RSI
    rsi_info = momentum.get("rsi", {})
    rsi_value = rsi_info.get("value", 0)
    rsi_signal = rsi_info.get("signal", "neutral")
    message += f"• RSI: {rsi_value:.1f} ({rsi_signal_emoji(rsi_signal)} {rsi_signal})\n"
    
    # MACD
    macd_info = momentum.get("macd", {})
    macd_signal = macd_info.get("signal", "neutral")
    message += f"• MACD: {macd_signal_emoji(macd_signal)} {macd_signal}\n"
    
    # Trend
    ma_info = trend.get("moving_averages", {})
    if ma_info.get("golden_cross"):
        message += "• 🥇 ALTIN KESİŞİM (Güçlü Boğa)\n"
    elif ma_info.get("death_cross"):
        message += "• 💀 ÖLÜM KESİŞİMİ (Güçlü Ayı)\n"
    
    trend_strength = trend.get("adx", {}).get("trend_strength", "weak")
    message += f"• Trend Gücü: {trend_strength_emoji(trend_strength)} {trend_strength}\n"
    
    # Price action
    price_action = analysis_result.get("price_action", {})
    pattern_count = price_action.get("active_patterns_count", 0)
    if pattern_count > 0:
        message += f"• Aktif Formasyon: {pattern_count} adet\n"
    
    # Fibonacci
    fibonacci = analysis_result.get("fibonacci", {})
    fib_relation = fibonacci.get("current_relation", {})
    if fib_relation:
        fib_level = list(fib_relation.keys())[0]
        message += f"• Fibonacci: %{fib_level} seviyesinde\n"
    
    # Sentiment
    sentiment = analysis_result.get("sentiment_analysis", {})
    sentiment_cat = sentiment.get("category", "NEUTRAL")
    message += f"• Sentiment: {sentiment_emoji(sentiment_cat)} {sentiment_cat}\n\n"
    
    # Risk Management
    risk_mgmt = analysis_result.get("risk_management", {})
    rr_analysis = risk_mgmt.get("risk_reward_analysis", {})
    rr_ratio = rr_analysis.get("best_rr_ratio", 0)
    
    message += f"🛡️ *RİSK YÖNETİMİ*\n"
    message += f"```\n"
    message += f"Risk/Ödül Oranı: {rr_ratio:.1f}:1\n"
    
    if rr_analysis.get("meets_minimum_rr"):
        message += f"✅ Minimum 2:1 R:R şartı sağlandı\n"
    else:
        message += f"⚠️ Minimum 2:1 R:R şartı sağlanmadı\n"
    
    # Position sizing example
    position = risk_mgmt.get("position_sizing", {})
    if position:
        message += f"\n$10K Portföy Örneği:\n"
        message += f"Pozisyon Büyüklüğü: ${position.get('position_value', 0):.0f}\n"
        message += f"Risk Miktarı: ${position.get('risk_amount', 0):.0f}\n"
        message += f"Stop Loss: %{position.get('stop_percent', 0):.1f}\n"
    
    message += f"```\n\n"
    
    # Trade Plan
    message += f"💼 *İŞLEM PLANI*\n"
    message += f"```\n"
    
    # Entry levels
    current_price = analysis_result.get("current_price", 0)
    message += f"Giriş Bölgesi:\n"
    message += f"• İdeal: ${current_price * 0.99:,.0f} - ${current_price * 1.01:,.0f}\n"
    
    # Stop loss
    stop_levels = risk_mgmt.get("stop_loss_levels", {})
    if stop_levels:
        stop_price = stop_levels.get("technical", current_price * 0.95)
        stop_percent = (1 - stop_price/current_price) * 100
        message += f"Stop Loss: ${stop_price:,.0f} (%{stop_percent:.1f})\n"
    
    # Targets
    if rr_analysis.get("best_target"):
        target = rr_analysis["best_target"]
        message += f"Hedef 1 ({target['type']}): ${target['price']:,.0f}\n"
        message += f"    (%{target['distance_percent']:.1f} kazanç)\n"
    
    message += f"```\n\n"
    
    # AI Insights
    ai_insights = analysis_result.get("ai_insights", "")
    if ai_insights and len(ai_insights) < 500:
        message += f"🤖 *GEMİNİ AI İÇGÖRÜLERİ*\n"
        message += f"_{ai_insights[:400]}..._\n\n"
    
    # Action Items
    message += f"⚡ *ACİL EYLEM PLANI*\n"
    message += f"1. ⏰ Fiyat alarmı kur: ${current_price:,.0f}\n"
    message += f"2. 📊 Tekrar kontrol: 4 saat sonra\n"
    
    recommended_action = analysis_result.get("final_signal", {}).get("recommended_action", "")
    if recommended_action:
        message += f"3. 🎯 {recommended_action}\n"
    
    # Final warning
    message += f"\n⚠️ *UYARI:* Bu analiz yatırım tavsiyesi değildir.\n"
    message += f"Kendi araştırmanızı yapın, riskleri anlayın.\n"
    
    # Footer
    message += f"\n---\n"
    message += f"🤖 PROMETHEUS AI ULTRA v1.0\n"
    message += f"7 Katmanlı Derin Analiz Sistemi\n"
    
    return message

def symbol_emoji(symbol: str) -> str:
    """Get emoji for symbol type"""
    symbol = symbol.upper()
    
    # Crypto
    if symbol in ["BTC", "ETH", "BNB", "XRP", "ADA", "SOL", "DOGE"]:
        return "₿"
    # Stocks
    elif symbol in ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NVDA"]:
        return "📈"
    # Forex
    elif any(forex in symbol for forex in ["EUR", "USD", "JPY", "GBP"]):
        return "💱"
    # Commodities
    elif symbol in ["GOLD", "XAUUSD", "SILVER", "XAGUSD"]:
        return "🥇"
    elif symbol in ["OIL", "CL", "BRENT"]:
        return "🛢️"
    else:
        return "📊"

def rsi_signal_emoji(signal: str) -> str:
    """Get emoji for RSI signal"""
    return {
        "oversold": "🟢",
        "overbought": "🔴",
        "bullish": "✅",
        "bearish": "❌",
        "neutral": "⚪"
    }.get(signal, "⚪")

def macd_signal_emoji(signal: str) -> str:
    """Get emoji for MACD signal"""
    return {
        "bullish": "✅",
        "bearish": "❌",
        "neutral": "⚪"
    }.get(signal, "⚪")

def trend_strength_emoji(strength: str) -> str:
    """Get emoji for trend strength"""
    return {
        "strong": "💪",
        "moderate": "👍",
        "weak": "👎"
    }.get(strength, "🤷")

def sentiment_emoji(sentiment: str) -> str:
    """Get emoji for sentiment"""
    return {
        "EXTREME_GREED": "😱",
        "GREED": "😀",
        "NEUTRAL": "😐",
        "FEAR": "😨",
        "EXTREME_FEAR": "😱"
    }.get(sentiment, "😐")

def format_quick_report(analysis_result: Dict[str, Any]) -> str:
    """Format quick analysis report"""
    symbol = analysis_result.get("symbol", "UNKNOWN")
    signal = analysis_result.get("final_signal", {}).get("decision", "HOLD")
    confidence = analysis_result.get("final_signal", {}).get("confidence_score", 0)
    current_price = analysis_result.get("current_price", 0)
    
    signal_emoji = {
        "STRONG_BUY": "🟢",
        "BUY": "✅",
        "HOLD": "🟡",
        "SELL": "🔴",
        "STRONG_SELL": "🛑"
    }.get(signal, "⚪")
    
    message = f"""
⚡ *{symbol} - HIZLI ANALİZ*
{signal_emoji} Sinyal: {signal}
📈 Güven: %{confidence}
💰 Fiyat: ${current_price:,.2f}

🎯 Özet:
"""
    
    # Add key points
    points = []
    
    # RSI
    rsi = analysis_result.get("technical_indicators", {}).get("momentum", {}).get("rsi", {})
    if rsi.get("value"):
        points.append(f"RSI: {rsi['value']:.1f}")
    
    # Trend
    trend = analysis_result.get("market_structure", {}).get("trend", {})
    if trend.get("primary"):
        points.append(f"Trend: {trend['primary']}")
    
    # Patterns
    patterns = analysis_result.get("price_action", {}).get("active_patterns_count", 0)
    if patterns > 0:
        points.append(f"{patterns} formasyon")
    
    # Add points to message
    for point in points:
        message += f"• {point}\n"
    
    # Recommendation
    action = analysis_result.get("final_signal", {}).get("recommended_action", "")
    if action:
        message += f"\n🎯 Tavsiye: {action}\n"
    
    message += f"\nℹ️ Detaylı analiz için: /analiz {symbol}"
    
    return message

def format_risk_report(analysis_result: Dict[str, Any]) -> str:
    """Format risk analysis report"""
    symbol = analysis_result.get("symbol", "UNKNOWN")
    risk_mgmt = analysis_result.get("risk_management", {})
    
    message = f"""
🛡️ *{symbol} - RİSK ANALİZİ*

📊 Volatilite:
"""
    
    # ATR
    atr_info = risk_mgmt.get("atr", {})
    if atr_info.get("value"):
        message += f"• ATR: ${atr_info['value']:.2f} (%{atr_info.get('percent', 0):.1f})\n"
    
    # Stop loss levels
    stop_levels = risk_mgmt.get("stop_loss_levels", {})
    if stop_levels:
        message += f"\n🛑 Stop Loss Seviyeleri:\n"
        for level_name, level_price in stop_levels.items():
            message += f"• {level_name}: ${level_price:,.2f}\n"
    
    # Position sizing
    position = risk_mgmt.get("position_sizing", {})
    if position:
        message += f"\n💰 Pozisyon Büyüklüğü:\n"
        message += f"• Risk/İşlem: %{position.get('risk_per_trade_percent', 0):.1f}\n"
        message += f"• Stop Mesafesi: %{position.get('stop_percent', 0):.1f}\n"
        message += f"• Pozisyon Değeri: ${position.get('position_value', 0):.0f}\n"
    
    # Risk factors
    risk_factors = risk_mgmt.get("risk_factors", [])
    if risk_factors:
        message += f"\n⚠️ Risk Faktörleri:\n"
        for factor in risk_factors[:3]:  # Show top 3
            message += f"• {factor}\n"
    
    # Var and Max Drawdown
    message += f"\n📈 Risk Ölçümleri:\n"
    message += f"• Max Drawdown: %{risk_mgmt.get('maximum_drawdown', 0):.1f}\n"
    message += f"• VaR (%95): %{risk_mgmt.get('var_95', 0):.1f}\n"
    
    return message
