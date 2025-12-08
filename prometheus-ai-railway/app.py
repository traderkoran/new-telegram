import logging
import os
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import numpy as np
from telegram import Update, constants
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import google.generativeai as genai
from flask import Flask
from threading import Thread
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import requests
from typing import Dict, Tuple

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
PORT = int(os.environ.get("PORT", 8080))

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        logging.warning(f"Gemini hatası: {e}")
        model = None
else:
    model = None

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

app = Flask(__name__)

@app.route('/')
def home():
    return "<html><body style='background:#0a0e27;color:#00ff88;text-align:center;padding:50px;font-family:monospace;'><h1>🦁 PROMETHEUS AI v10.0</h1><h2>Railway Edition</h2><p>STATUS: ONLINE ⚡</p></body></html>"

@app.route('/health')
def health():
    return {'status': 'ok'}

def run_flask():
    app.run(host='0.0.0.0', port=PORT)

def keep_alive():
    Thread(target=run_flask, daemon=True).start()
    logging.info(f"Flask başlatıldı: {PORT}")

PROMETHEUS_PROMPT = """
SEN: PROMETHEUS AI v10.0 - Ultra Yatırım Analiz Sistemi

7 KATMAN ANALİZ YAP:
1. Fiyat Hareketi (Mum formasyonları)
2. Teknik Göstergeler (RSI, MACD, SMA...)
3. Fibonacci Seviyeleri
4. Piyasa Yapısı
5. Temel Analiz
6. Sentiment
7. Risk Yönetimi

ÇIKTI FORMATI:
## 🎯 YÖNETİCİ ÖZETİ
**KARAR:** [🟢 GÜÇLÜ AL / 🟡 AL / ⚪ BEKLE / 🟠 SAT / 🔴 GÜÇLÜ SAT]
**Güven:** %XX
**Risk:** [DÜŞÜK/ORTA/YÜKSEK]
**Tez:** [2 cümle]

## 📊 DETAYLI ANALİZ
[Tüm katmanları detaylı açıkla]

## 💼 İŞLEM PLANI
Giriş: $XX
Stop-Loss: $XX (-%X risk)
Hedef 1: $XX (R:R X:1)
Hedef 2: $XX (R:R X:1)

$10K hesap: $XXX pozisyon

## ⚠️ RİSK UYARISI
Sermayenin %2'sinden fazlasını riske atma!

DETAYLI, PROFESYONEL, EYLEME DÖNÜŞTÜRÜLEBILIR ANALİZ YAP!
"""

def calc_indicators(df):
    try:
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        
        df['RSI'] = ta.rsi(df['Close'], length=14)
        
        macd = ta.macd(df['Close'])
        if macd is not None:
            df['MACD'] = macd['MACD_12_26_9']
            df['MACD_SIGNAL'] = macd['MACDs_12_26_9']
        
        for l in [20, 50, 200]:
            if len(df) >= l:
                df[f'SMA_{l}'] = ta.sma(df['Close'], length=l)
        
        bb = ta.bbands(df['Close'], length=20)
        if bb is not None:
            df['BB_UPPER'] = bb['BBU_20_2.0']
            df['BB_LOWER'] = bb['BBL_20_2.0']
        
        atr = ta.atr(df['High'], df['Low'], df['Close'])
        df['ATR'] = atr if atr is not None else 0
        
        df['OBV'] = ta.obv(df['Close'], df['Volume'])
        df['VOL_SMA'] = ta.sma(df['Volume'], length=20)
        df['VOL_RATIO'] = df['Volume'] / df['VOL_SMA'].replace(0, 1)
        
        return df
    except Exception as e:
        logging.error(f"Gösterge hatası: {e}")
        return df

def detect_patterns(df):
    patterns = {'bullish': [], 'bearish': []}
    try:
        for i in range(max(0, len(df)-3), len(df)):
            c = df.iloc[i]
            body = abs(c['Close'] - c['Open'])
            range_val = c['High'] - c['Low']
            if range_val == 0:
                continue
            lower = min(c['Open'], c['Close']) - c['Low']
            
            if body <= range_val * 0.1 and lower > body * 3:
                patterns['bullish'].append("Dragonfly Doji")
            elif lower > body * 2:
                if c['Close'] > c['Open']:
                    patterns['bullish'].append("Hammer ⭐")
        
        if len(df) >= 2:
            prev, curr = df.iloc[-2], df.iloc[-1]
            if (prev['Close'] < prev['Open'] and curr['Close'] > curr['Open'] and
                curr['Close'] > prev['Open'] and curr['Open'] < prev['Close']):
                patterns['bullish'].append("Bullish Engulfing ⭐⭐")
    except:
        pass
    return patterns

def get_fib(df):
    try:
        high, low = df['High'].tail(100).max(), df['Low'].tail(100).min()
        diff = high - low
        return {
            '61.8': high - 0.618 * diff,
            '50.0': high - 0.5 * diff,
            '38.2': high - 0.382 * diff
        }
    except:
        return {}

def get_sr(df):
    try:
        r = df['High'].tail(50).nlargest(3).mean()
        s = df['Low'].tail(50).nsmallest(3).mean()
        return s, r
    except:
        return None, None

def get_fear_greed():
    try:
        r = requests.get("https://api.alternative.me/fng/", timeout=3)
        data = r.json()['data'][0]
        return int(data['value']), data['value_classification']
    except:
        return None, None

def convert_symbol(sym):
    crypto = {"BTC": "BTC-USD", "ETH": "ETH-USD", "SOL": "SOL-USD", "AVAX": "AVAX-USD", "XRP": "XRP-USD"}
    commodity = {"ALTIN": "GC=F", "PETROL": "CL=F", "GUMUS": "SI=F"}
    if sym in crypto:
        return crypto[sym]
    elif sym in commodity:
        return commodity[sym]
    elif ".IS" not in sym and len(sym) <= 6:
        return f"{sym}.IS"
    return sym

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = """
🦁 **PROMETHEUS AI v10.0**

Efsanevi 7 Katmanlı Analiz Sistemi

📊 **KOMUTLAR:**
/analiz BTC - Tam detaylı analiz
/hizli BTC - Hızlı özet
BTC - Direkt sembol

✅ Kripto, Hisse, Forex, Emtia
⚡ Gemini AI Powered
    """
    await update.message.reply_text(msg, parse_mode=constants.ParseMode.MARKDOWN)

async def quick_analysis(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text.upper().replace("/HIZLI", "").strip()
    if not user_msg:
        await update.message.reply_text("Örn: `/hizli BTC`")
        return
    
    status = await update.message.reply_text(f"⚡ {user_msg} analizi...")
    symbol = convert_symbol(user_msg)
    
    try:
        df = yf.download(symbol, period="3mo", interval="1d", progress=False)
        if df.empty:
            await status.edit_text(f"❌ Veri yok: {user_msg}")
            return
        
        df = calc_indicators(df)
        last = df.iloc[-1]
        
        score = 0
        factors = []
        
        if 'SMA_200' in df.columns and last['Close'] > last['SMA_200']:
            score += 20
            factors.append("✅ SMA 200 üstünde")
        else:
            score -= 20
            factors.append("❌ SMA 200 altında")
        
        rsi = last.get('RSI', 50)
        if rsi < 30:
            score += 25
            factors.append(f"✅ RSI aşırı satım ({rsi:.1f})")
        elif rsi > 70:
            score -= 25
            factors.append(f"❌ RSI aşırı alım ({rsi:.1f})")
        
        decision = "🟢 AL" if score >= 20 else "🔴 SAT" if score <= -20 else "⚪ BEKLE"
        
        report = f"""
⚡ **{user_msg}** Hızlı Analiz

**Karar:** {decision}
**Skor:** {score}/100
**Fiyat:** ${last['Close']:.2f}
**RSI:** {rsi:.1f}

**Faktörler:**
{chr(10).join(factors)}

Detay: /analiz {user_msg}
        """
        await status.edit_text(report, parse_mode=constants.ParseMode.MARKDOWN)
    except Exception as e:
        await status.edit_text(f"⚠️ Hata: {str(e)}")

async def full_analysis(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text.upper().replace("/ANALIZ", "").replace("/ANALİZ", "").strip()
    if not user_msg:
        await update.message.reply_text("Örn: `/analiz BTC`")
        return
    
    status = await update.message.reply_text(f"🔍 {user_msg} detaylı analiz...")
    symbol = convert_symbol(user_msg)
    
    try:
        df = yf.download(symbol, period="1y", interval="1d", progress=False)
        if df.empty:
            await status.edit_text(f"❌ Veri yok: {user_msg}")
            return
        
        df = calc_indicators(df)
        last = df.iloc[-1]
        patterns = detect_patterns(df)
        fib = get_fib(df)
        s, r = get_sr(df)
        fg, fg_text = get_fear_greed()
        
        if not model:
            await status.edit_text("⚠️ Gemini API anahtarı yok!")
            return
        
        data = f"""
VARLIK: {user_msg}
Fiyat: ${last['Close']:.2f}
24s Değişim: {((last['Close']-df.iloc[-2]['Close'])/df.iloc[-2]['Close']*100):.2f}%

MUM FORMASYONLARI:
Bullish: {', '.join(patterns['bullish']) if patterns['bullish'] else 'Yok'}
Bearish: {', '.join(patterns['bearish']) if patterns['bearish'] else 'Yok'}

TEKNİK GÖSTERGELER:
RSI: {last.get('RSI', 0):.1f} {'(Aşırı Satım)' if last.get('RSI', 50) < 30 else '(Aşırı Alım)' if last.get('RSI', 50) > 70 else ''}
MACD: {last.get('MACD', 0):.2f}
SMA 20: ${last.get('SMA_20', 0):.2f} {'(Üstünde ✅)' if last['Close'] > last.get('SMA_20', 0) else '(Altında ❌)'}
SMA 50: ${last.get('SMA_50', 0):.2f} {'(Üstünde ✅)' if last['Close'] > last.get('SMA_50', 0) else '(Altında ❌)'}
SMA 200: ${last.get('SMA_200', 0):.2f} {'(Üstünde ✅)' if last['Close'] > last.get('SMA_200', 0) else '(Altında ❌)'}
Bollinger: ${last.get('BB_UPPER', 0):.2f} / ${last.get('BB_LOWER', 0):.2f}
ATR: {last.get('ATR', 0):.2f}
Volume Ratio: {last.get('VOL_RATIO', 1):.2f}x

FIBONACCI:
61.8% (Altın): ${fib.get('61.8', 0):.2f}
50.0%: ${fib.get('50.0', 0):.2f}

DESTEK/DİRENÇ:
Destek: ${s if s else 0:.2f}
Direnç: ${r if r else 0:.2f}

SENTIMENT:
Fear&Greed: {fg}/100 ({fg_text}) {'' if not fg else '⚠️ FIRSATMIŞ!' if fg < 30 else '⚠️ DİKKAT!' if fg > 70 else ''}

PROMETHEUS AI FORMATINDA 7 KATMAN ANALİZ YAP!
        """
        
        response = model.generate_content(PROMETHEUS_PROMPT + "\n\n" + data)
        result = response.text
        
        if len(result) > 4000:
            parts = [result[i:i+4000] for i in range(0, len(result), 4000)]
            await status.edit_text(parts[0], parse_mode=constants.ParseMode.MARKDOWN)
            for part in parts[1:]:
                await update.message.reply_text(part, parse_mode=constants.ParseMode.MARKDOWN)
        else:
            await status.edit_text(result, parse_mode=constants.ParseMode.MARKDOWN)
    
    except Exception as e:
        logging.error(f"Analiz hatası: {e}")
        await status.edit_text(f"⚠️ Hata: {str(e)}")

def start_bot():
    if not TELEGRAM_TOKEN:
        logging.error("❌ TELEGRAM_TOKEN yok!")
        return
    
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("analiz", full_analysis))
    application.add_handler(CommandHandler("hizli", quick_analysis))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, full_analysis))
    
    logging.info("🦁 PROMETHEUS AI başlatılıyor...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    keep_alive()
    start_bot()
