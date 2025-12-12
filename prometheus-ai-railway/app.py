#!/usr/bin/env python3
"""
PROMETHEUS AI ULTRA v1.0 - Elite Investment Analysis Bot
Integrates both PROMETHEUS AI v6.0 and Efsanevi Yatırım Yeteneği systems
"""

import os
import logging
import asyncio
from typing import Dict, Any, Optional
from datetime import datetime

from flask import Flask, request, jsonify
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler, 
    filters, ContextTypes, CallbackQueryHandler
)
import google.generativeai as genai

from config import config
from analysis_engine.comprehensive_analyzer import ComprehensiveAnalyzer
from data_fetchers.universal_client import UniversalDataClient
from utils.formatters import format_analysis_report

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize Flask app for Render
app = Flask(__name__)

# Initialize components
data_client = UniversalDataClient()
analyzer = ComprehensiveAnalyzer()

# Initialize Gemini AI
genai.configure(api_key=config.GEMINI_API_KEY)
gemini_model = genai.GenerativeModel(config.GEMINI_MODEL)

class PrometheusUltraBot:
    def __init__(self):
        self.user_sessions: Dict[int, Dict] = {}
        self.analysis_cache: Dict[str, Dict] = {}
        
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        user = update.effective_user
        welcome_message = f"""
🤖 *PROMETHEUS AI ULTRA v1.0 - Elite Investment Oracle*

*Merhaba {user.first_name}!* 🎯

Ben, 7 katmanlı derin analiz sistemi ile donatılmış en gelişmiş yatırım asistanıyım.

🔍 *Desteklenen Analizler:*
• 38+ Mum Formasyonu
• 50+ Teknik Gösterge
• Fibonacci & Matematiksel Analiz
• Piyasa Yapısı & Likidite
• Temel Analiz (Hisse/Kripto/Forex)
• Sentiment & Psikoloji
• Risk Yönetimi & Pozisyon Boyutu

📊 *Desteklenen Varlıklar:*
• Kripto: BTC, ETH, SOL, BNB, XRP...
• Hisse: AAPL, TSLA, MSFT, GOOGL...
• Forex: EURUSD, GBPUSD, USDJPY...
• Emtia: ALTIN, PETROL

📈 *Komutlar:*
/start - Başlangıç mesajı
/analiz [sembol] - Tam 7 katman analiz
/hizli [sembol] - Hızlı özet analiz
/risk [sembol] - Risk analizi
/yardim - Tüm komutlar

💡 *Örnek:* `/analiz BTC` veya sadece `BTC` yazın
        """
        
        keyboard = [
            [
                InlineKeyboardButton("📊 Tam Analiz", callback_data="menu_full"),
                InlineKeyboardButton("⚡ Hızlı Analiz", callback_data="menu_quick")
            ],
            [
                InlineKeyboardButton("🎯 Popüler", callback_data="menu_popular"),
                InlineKeyboardButton("📈 Örnek", callback_data="menu_example")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            welcome_message,
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
    
    async def analyze_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /analiz command"""
        if not context.args:
            await update.message.reply_text(
                "⚠️ Lütfen bir sembol belirtin.\nÖrnek: `/analiz BTC` veya `/analiz AAPL`",
                parse_mode='Markdown'
            )
            return
        
        symbol = context.args[0].upper()
        await self.perform_analysis(update, symbol, "full")
    
    async def quick_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /hizli command"""
        if not context.args:
            await update.message.reply_text(
                "⚠️ Lütfen bir sembol belirtin.\nÖrnek: `/hizli BTC`",
                parse_mode='Markdown'
            )
            return
        
        symbol = context.args[0].upper()
        await self.perform_analysis(update, symbol, "quick")
    
    async def risk_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /risk command"""
        if not context.args:
            await update.message.reply_text(
                "⚠️ Lütfen bir sembol belirtin.\nÖrnek: `/risk BTC`",
                parse_mode='Markdown'
            )
            return
        
        symbol = context.args[0].upper()
        await self.perform_analysis(update, symbol, "risk")
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /yardim command"""
        help_text = """
🆘 *Yardım - PROMETHEUS AI ULTRA*

*Temel Komutlar:*
/start - Botu başlat
/analiz [sembol] - Tam detaylı 7 katman analiz
/hizli [sembol] - Hızlı özet analiz
/risk [sembol] - Risk yönetimi analizi
/yardim - Bu mesajı göster

*Kullanım Örnekleri:*
• `/analiz BTC` - Bitcoin tam analiz
• `/hizli AAPL` - Apple hızlı analiz
• `ETH` - Direkt sembol yazımı
• `/risk TSLA` - Tesla risk analizi

*Analiz Katmanları:*
1. 📊 Fiyat Hareketi (38+ formasyon)
2. 🎯 Teknik Göstergeler (50+ gösterge)
3. 🔢 Fibonacci & Matematik
4. 🏛️ Piyasa Yapısı
5. 📈 Temel Analiz
6. 😊 Sentiment Analiz
7. 🛡️ Risk Yönetimi

*Desteklenen Semboller:*
• Kripto: BTC, ETH, BNB, XRP, SOL, ADA, DOGE...
• Hisse: AAPL, TSLA, MSFT, GOOGL, AMZN, META...
• Forex: EURUSD, GBPUSD, USDJPY, AUDUSD...
• Emtia: ALTIN, PETROL, GUMUS
        """
        
        await update.message.reply_text(help_text, parse_mode='Markdown')
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle direct symbol messages"""
        text = update.message.text.upper().strip()
        
        # Check if it's a known symbol
        all_symbols = (
            config.CRYPTO_SYMBOLS + 
            config.STOCK_SYMBOLS + 
            [pair[:3] for pair in config.FOREX_PAIRS] +
            [pair[3:] for pair in config.FOREX_PAIRS]
        )
        
        if text in all_symbols or any(text in pair for pair in config.FOREX_PAIRS):
            await self.perform_analysis(update, text, "quick")
        else:
            await update.message.reply_text(
                f"❌ '{text}' sembolünü tanımıyorum.\n"
                f"Desteklenen semboller için /yardim yazın."
            )
    
    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle button callbacks"""
        query = update.callback_query
        await query.answer()
        
        data = query.data
        
        if data == "menu_full":
            await query.edit_message_text(
                "📊 Tam analiz için sembol yazın.\nÖrnek: `BTC` veya `AAPL`",
                parse_mode='Markdown'
            )
        elif data == "menu_quick":
            await query.edit_message_text(
                "⚡ Hızlı analiz için sembol yazın.\nÖrnek: `ETH` veya `TSLA`",
                parse_mode='Markdown'
            )
        elif data == "menu_popular":
            keyboard = [
                [
                    InlineKeyboardButton("BTC", callback_data="symbol_BTC"),
                    InlineKeyboardButton("ETH", callback_data="symbol_ETH"),
                    InlineKeyboardButton("SOL", callback_data="symbol_SOL")
                ],
                [
                    InlineKeyboardButton("AAPL", callback_data="symbol_AAPL"),
                    InlineKeyboardButton("TSLA", callback_data="symbol_TSLA"),
                    InlineKeyboardButton("MSFT", callback_data="symbol_MSFT")
                ],
                [
                    InlineKeyboardButton("EURUSD", callback_data="symbol_EURUSD"),
                    InlineKeyboardButton("ALTIN", callback_data="symbol_XAUUSD"),
                    InlineKeyboardButton("PETROL", callback_data="symbol_OIL")
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.edit_message_text(
                "🎯 Popüler sembollerden birini seçin:",
                reply_markup=reply_markup
            )
        elif data == "menu_example":
            example_report = """
📈 *Örnek Analiz Çıktısı:*

🎯 *YÖNETİCİ ÖZETİ*
Sinyal: 🟢 GÜÇLÜ AL
Güven: %84
Risk: ORTA
Zaman: 1-4 hafta

📊 *7 KATMAN ANALİZ*
1. Fiyat: Bullish Engulfing + Hammer
2. Teknik: RSI 42 (neutral), MACD bullish cross
3. Fibonacci: %61.8 support holding
4. Yapı: Uptrend HH+HL
5. Temel: Strong fundamentals
6. Sentiment: Fear & Greed 45 (Fear)
7. Risk: R:R = 3.2:1

💼 *İŞLEM PLANI*
Giriş: $45,200 - $45,800
Stop: $42,500 (-6%)
Hedef: $52,000 (+15%)

*$10K portföy için:*
Pozisyon: $3,300
Risk: $200 (2%)
            """
            
            await query.edit_message_text(
                example_report,
                parse_mode='Markdown'
            )
        elif data.startswith("symbol_"):
            symbol = data.replace("symbol_", "")
            await self.perform_analysis_callback(query, symbol, "full")
    
    async def perform_analysis(self, update: Update, symbol: str, analysis_type: str):
        """Perform analysis and send results"""
        try:
            # Send initial message
            message = await update.message.reply_text(
                f"🔍 *{symbol}* analiz ediliyor...\n"
                f"7 katmanlı tarama başlatıldı ⚡",
                parse_mode='Markdown'
            )
            
            # Get data
            price_data = await data_client.fetch_data(symbol)
            
            if price_data is None or price_data.empty:
                await message.edit_text(
                    f"❌ *{symbol}* için veri bulunamadı.\n"
                    f"Lütfen sembolü kontrol edin.",
                    parse_mode='Markdown'
                )
                return
            
            # Perform analysis
            analysis_result = analyzer.analyze(symbol, price_data, analysis_type)
            
            # Enhance with Gemini AI
            enhanced_result = await self.enhance_with_ai(analysis_result, symbol)
            
            # Format and send report
            report = format_analysis_report(enhanced_result)
            
            # Split long messages
            if len(report) > 4000:
                parts = [report[i:i+4000] for i in range(0, len(report), 4000)]
                for i, part in enumerate(parts):
                    if i == 0:
                        await message.edit_text(part, parse_mode='Markdown')
                    else:
                        await update.message.reply_text(part, parse_mode='Markdown')
            else:
                await message.edit_text(report, parse_mode='Markdown')
                
        except Exception as e:
            logger.error(f"Analysis error: {e}", exc_info=True)
            error_msg = (
                f"⚠️ Analiz sırasında hata oluştu:\n"
                f"`{str(e)[:100]}`\n\n"
                f"Lütfen daha sonra tekrar deneyin."
            )
            
            if 'message' in locals():
                await message.edit_text(error_msg, parse_mode='Markdown')
            else:
                await update.message.reply_text(error_msg, parse_mode='Markdown')
    
    async def perform_analysis_callback(self, query, symbol: str, analysis_type: str):
        """Perform analysis for callback queries"""
        try:
            await query.edit_message_text(
                f"🔍 *{symbol}* analiz ediliyor...\n⏳ Lütfen bekleyin",
                parse_mode='Markdown'
            )
            
            price_data = await data_client.fetch_data(symbol)
            
            if price_data is None or price_data.empty:
                await query.edit_message_text(
                    f"❌ *{symbol}* için veri bulunamadı.",
                    parse_mode='Markdown'
                )
                return
            
            analysis_result = analyzer.analyze(symbol, price_data, analysis_type)
            enhanced_result = await self.enhance_with_ai(analysis_result, symbol)
            report = format_analysis_report(enhanced_result)
            
            await query.edit_message_text(report, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"Callback analysis error: {e}")
            await query.edit_message_text(
                f"❌ Hata: {str(e)[:100]}",
                parse_mode='Markdown'
            )
    
    async def enhance_with_ai(self, analysis_result: Dict, symbol: str) -> Dict:
        """Enhance analysis with Gemini AI insights"""
        try:
            prompt = f"""
            SEN PROMETHEUS AI ULTRA'SIN - En gelişmiş finansal analiz sistemi.
            
            SEMBOL: {symbol}
            ANALİZ VERİLERİ: {str(analysis_result)[:2000]}
            
            Lütfen bu analizi geliştir:
            1. Warren Buffett'in değer yatırımı perspektifinden değerlendir
            2. George Soros'un makro zamanlama teorisini uygula
            3. Jim Simons'ın matematiksel modelleme yaklaşımını ekle
            4. Ray Dalio'nun All-Weather risk yönetimini dahil et
            5. Paul Tudor Jones'un makro+teknik sentezini yap
            
            Özellikle şunlara odaklan:
            - Asimetrik risk/ödül fırsatları
            - Piyasa refleksivitesi
            - Olası kara kuğu senaryoları
            - Optimal pozisyon büyüklüğü
            
            Analizi Türkçe olarak geliştir.
            """
            
            response = await gemini_model.generate_content_async(prompt)
            analysis_result['ai_insights'] = response.text
            
            return analysis_result
            
        except Exception as e:
            logger.error(f"Gemini AI error: {e}")
            analysis_result['ai_insights'] = "AI geliştirmesi geçici olarak kullanılamıyor."
            return analysis_result

# Initialize bot
bot = PrometheusUltraBot()

# Flask routes for Render
@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for Render"""
    return jsonify({
        "status": "healthy",
        "service": "Prometheus AI Ultra Bot",
        "timestamp": datetime.now().isoformat()
    }), 200

@app.route('/webhook', methods=['POST'])
def webhook():
    """Webhook endpoint for Telegram (if using webhooks)"""
    # For polling mode, this isn't used
    return jsonify({"status": "webhook_not_used"}), 200

@app.route('/')
def index():
    """Main page"""
    return """
    <html>
        <head>
            <title>PROMETHEUS AI ULTRA v1.0</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                }
                .container {
                    background: rgba(255, 255, 255, 0.1);
                    backdrop-filter: blur(10px);
                    border-radius: 15px;
                    padding: 30px;
                    margin-top: 50px;
                }
                h1 {
                    text-align: center;
                    margin-bottom: 30px;
                }
                .status {
                    background: rgba(0, 255, 0, 0.2);
                    padding: 10px;
                    border-radius: 5px;
                    text-align: center;
                    margin: 20px 0;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🤖 PROMETHEUS AI ULTRA v1.0</h1>
                <p>Elite Investment Analysis Bot</p>
                
                <div class="status">
                    ✅ System Status: OPERATIONAL
                </div>
                
                <h3>🎯 Features:</h3>
                <ul>
                    <li>7-Layer Deep Analysis System</li>
                    <li>38+ Candlestick Patterns</li>
                    <li>50+ Technical Indicators</li>
                    <li>Fibonacci & Mathematical Analysis</li>
                    <li>Market Structure & Liquidity Analysis</li>
                    <li>Fundamental Analysis (Stocks/Crypto/Forex)</li>
                    <li>Sentiment & Psychology Analysis</li>
                    <li>Risk Management & Position Sizing</li>
                    <li>Gemini 1.5 Flash AI Powered</li>
                </ul>
                
                <p>🚀 <strong>Telegram Bot:</strong> @PrometheusUltraBot</p>
                <p>📊 <strong>Analysis Examples:</strong> /analiz BTC, /hizli AAPL</p>
                <p>⚡ <strong>Powered by:</strong> Render + Gemini AI</p>
            </div>
        </body>
    </html>
    """

async def main():
    """Main function to run the bot"""
    # Create Telegram application
    application = Application.builder().token(config.TELEGRAM_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", bot.start_command))
    application.add_handler(CommandHandler("analiz", bot.analyze_command))
    application.add_handler(CommandHandler("hizli", bot.quick_command))
    application.add_handler(CommandHandler("risk", bot.risk_command))
    application.add_handler(CommandHandler("yardim", bot.help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, bot.handle_message))
    application.add_handler(CallbackQueryHandler(bot.handle_callback))
    
    # Start polling
    await application.initialize()
    await application.start()
    
    logger.info("🤖 PROMETHEUS AI ULTRA Bot started!")
    
    # Keep running
    await application.updater.start_polling()
    
    # Run Flask app in separate thread
    import threading
    flask_thread = threading.Thread(
        target=lambda: app.run(
            host='0.0.0.0',
            port=int(os.environ.get('PORT', 5000)),
            debug=False,
            use_reloader=False
        )
    )
    flask_thread.start()
    
    # Wait for shutdown
    await asyncio.Event().wait()

if __name__ == '__main__':
    # Check for required environment variables
    if not config.TELEGRAM_TOKEN or not config.GEMINI_API_KEY:
        logger.error("❌ TELEGRAM_TOKEN ve GEMINI_API_KEY environment variables gereklidir!")
        exit(1)
    
    # Run the bot
    asyncio.run(main())
