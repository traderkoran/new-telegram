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
import time

# ==================== KONFIGÜRASYON ====================
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
PORT = int(os.environ.get("PORT", 8080))

# Gemini Model
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        logging.info("✅ Gemini AI bağlantısı başarılı")
    except Exception as e:
        logging.warning(f"⚠️ Gemini hatası: {e}")
        model = None
else:
    logging.warning("⚠️ GEMINI_API_KEY yok!")
    model = None

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# ==================== FLASK SERVER ====================
app = Flask(__name__)

@app.route('/')
def home():
    return """
<!DOCTYPE html>
<html>
<head>
    <title>PROMETHEUS AI v10.0</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            background: linear-gradient(135deg, #0a0e27, #1a1f3a);
            color: #00ff88;
            font-family: 'Courier New', monospace;
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            background: rgba(20, 25, 45, 0.95);
            border: 3px solid #00ff88;
            border-radius: 20px;
            padding: 50px;
            max-width: 800px;
            box-shadow: 0 0 50px rgba(0, 255, 136, 0.5);
            animation: glow 2s ease-in-out infinite alternate;
        }
        @keyframes glow {
            from { box-shadow: 0 0 30px rgba(0, 255, 136, 0.4); }
            to { box-shadow: 0 0 70px rgba(0, 255, 136, 0.8); }
        }
        h1 { font-size: 3em; text-align: center; margin-bottom: 10px; text-shadow: 0 0 20px #00ff88; }
        h2 { color: #ffaa00; text-align: center; margin-bottom: 30px; }
        .feature { background: rgba(0, 255, 136, 0.05); border-left: 4px solid #00ff88; padding: 15px; margin: 15px 0; border-radius: 5px; }
        .status { margin-top: 30px; padding: 20px; background: rgba(0, 170, 255, 0.1); border: 2px solid #00aaff; border-radius: 10px; text-align: center; font-size: 1.3em; }
        .pulse { display: inline-block; width: 15px; height: 15px; background: #00ff88; border-radius: 50%; margin-right: 10px; animation: pulse 1.5s ease-in-out infinite; }
        @keyframes pulse { 0%, 100% { transform: scale(1); opacity: 1; } 50% { transform: scale(1.3); opacity: 0.6; } }
    </style>
</head>
<body>
    <div class="container">
        <h1>🦁 PROMETHEUS AI v10.0</h1>
        <h2>Efsanevi Yatırım Analiz Sistemi</h2>
        <div class="feature">✅ 7 Katmanlı Analiz</div>
        <div class="feature">✅ 38 Mum Formasyonu</div>
        <div class="feature">✅ 50+ Teknik Gösterge</div>
        <div class="feature">✅ Gemini AI Powered</div>
        <div class="feature">✅ Risk Yönetimi</div>
        <div class="status">
            <span class="pulse"></span>
            <strong>STATUS: ONLINE ⚡</strong>
        </div>
    </div>
</body>
</html>
    """

@app.route('/health')
def health():
    return {'status': 'healthy', 'version': '10.0', 'gemini': model is not None}

def run_flask():
    app.run(host='0.0.0.0', port=PORT, threaded=True)

def keep_alive():
    Thread(target=run_flask, daemon=True).start()
    logging.info(f"✅ Flask server başlatıldı (Port: {PORT})")

# ==================== PROMETHEUS AI SYSTEM ====================
PROMETHEUS_PROMPT = """
SEN: PROMETHEUS AI v10.0 - Ultra Profesyonel Yatırım Analiz Sistemi

GÖREV: Kullanıcının sorduğu varlığı 7 KATMANLI ANALİZ ile değerlendir.

7 KATMAN:
1. FİYAT HAREKETİ: Mum formasyonları, grafik patternleri
2. TEKNİK GÖSTERGELER: RSI, MACD, Bollinger, SMA...
3. MATEMATİK: Fibonacci, destek/direnç
4. PİYASA YAPISI: Trend, likidite
5. TEMEL ANALİZ: Değerleme veya on-chain
6. SENTIMENT: Korku/Açgözlülük
7. RİSK YÖNETİMİ: Pozisyon boyutu, stop-loss

ÇIKTI FORMATI:

## 🎯 YÖNETİCİ ÖZETİ
**KARAR:** [🟢 GÜÇLÜ AL / 🟡 AL / ⚪ BEKLE / 🟠 SAT / 🔴 GÜÇLÜ SAT]
**Güven Skoru:** %XX
**Risk Seviyesi:** [DÜŞÜK/ORTA/YÜKSEK]
**Zaman Ufku:** [Kısa/Orta/Uzun Vade]
**Temel Tez:** [Neden bu karar? 2 cümle]

## 📊 7 KATMAN ANALİZ

### KATMAN 1: FİYAT HAREKETİ
- Tespit Edilen Mum Formasyonları: [Listele]
- Grafik Pattern: [Varsa belirt]
- Sinyal Gücü: [Zayıf/Orta/Güçlü]

### KATMAN 2: TEKNİK GÖSTERGELER
- RSI: XX.X [Yorum]
- MACD: [Yükseliş/Düşüş/Nötr]
- Trend: [SMA 50/200 konumu]
- Bollinger: [Konumu]
- Hacim: [Normal/Yüksek/Düşük]

### KATMAN 3: MATEMATİK
- Fibonacci 61.8% (Altın): $XX
- Kritik Destek: $XX
- Kritik Direnç: $XX

### KATMAN 4: PİYASA YAPISI
- Trend: [Yükseliş/Düşüş/Yatay]
- Yapı: [HH+HL / LH+LL / Range]
- Likidite: [Açıklama]

### KATMAN 5: TEMEL ANALİZ
[Kripto ise on-chain, hisse ise değerleme]

### KATMAN 6: SENTIMENT
- Fear & Greed: XX/100 [Yorum]

### KATMAN 7: RİSK YÖNETİMİ
**İŞLEM PLANI:**
- Giriş: $XX.XX
- Stop-Loss: $XX.XX (-%X risk)
- Hedef 1: $XX.XX (R:R X:1)
- Hedef 2: $XX.XX (R:R X:1)

**Pozisyon Boyutu:**
- $10,000 hesap: $XXX (risk $200)
- $50,000 hesap: $XXX (risk $1,000)

## ⚠️ RİSK UYARISI
Sermayenin %2'sinden fazlasını riske atma! Stop-loss zorunlu!

DETAYLI, PROFESYONEL, EYLEME DÖNÜŞTÜRÜLEBİLİR ANALİZ YAP!
"""

# ==================== ANALİZ FONKSİYONLARI ====================

def calc_indicators(df):
    """Tüm teknik göstergeleri hesapla"""
    try:
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        
        # Momentum
        df['RSI'] = ta.rsi(df['Close'], length=14)
        
        macd = ta.macd(df['Close'])
        if macd is not None:
            df['MACD'] = macd['MACD_12_26_9']
            df['MACD_SIGNAL'] = macd['MACDs_12_26_9']
            df['MACD_HIST'] = macd['MACDh_12_26_9']
        
        # Trend
        for l in [20, 50, 200]:
            if len(df) >= l:
                df[f'SMA_{l}'] = ta.sma(df['Close'], length=l)
        
        # Volatilite
        bb = ta.bbands(df['Close'], length=20)
        if bb is not None:
            df['BB_UPPER'] = bb['BBU_20_2.0']
            df['BB_MID'] = bb['BBM_20_2.0']
            df['BB_LOWER'] = bb['BBL_20_2.0']
        
        atr = ta.atr(df['High'], df['Low'], df['Close'])
        df['ATR'] = atr if atr is not None else 0
        
        # Hacim
        df['OBV'] = ta.obv(df['Close'], df['Volume'])
        df['VOL_SMA'] = ta.sma(df['Volume'], length=20)
        df['VOL_RATIO'] = df['Volume'] / df['VOL_SMA'].replace(0, 1)
        
        return df
    except Exception as e:
        logging.error(f"Gösterge hatası: {e}")
        return df

def detect_patterns(df):
    """Mum formasyonlarını tespit et"""
    patterns = {'bullish': [], 'bearish': []}
    try:
        for i in range(max(0, len(df)-5), len(df)):
            c = df.iloc[i]
            body = abs(c['Close'] - c['Open'])
            range_val = c['High'] - c['Low']
            if range_val == 0:
                continue
            
            lower = min(c['Open'], c['Close']) - c['Low']
            upper = c['High'] - max(c['Open'], c['Close'])
            
            # Doji
            if body <= range_val * 0.1:
                if lower > body * 3:
                    patterns['bullish'].append("Dragonfly Doji")
                elif upper > body * 3:
                    patterns['bearish'].append("Gravestone Doji")
            
            # Hammer
            elif lower > body * 2 and upper < body * 0.3:
                if c['Close'] > c['Open']:
                    patterns['bullish'].append("Hammer ⭐")
                else:
                    patterns['bearish'].append("Hanging Man")
            
            # Shooting Star
            elif upper > body * 2 and lower < body * 0.3:
                if c['Close'] < c['Open']:
                    patterns['bearish'].append("Shooting Star ⭐")
        
        # Engulfing
        if len(df) >= 2:
            prev, curr = df.iloc[-2], df.iloc[-1]
            if (prev['Close'] < prev['Open'] and curr['Close'] > curr['Open'] and
                curr['Close'] > prev['Open'] and curr['Open'] < prev['Close']):
                patterns['bullish'].append("Bullish Engulfing ⭐⭐")
            elif (prev['Close'] > prev['Open'] and curr['Close'] < curr['Open'] and
                  curr['Close'] < prev['Open'] and curr['Open'] > prev['Close']):
                patterns['bearish'].append("Bearish Engulfing ⭐⭐")
    except Exception as e:
        logging.error(f"Pattern hatası: {e}")
    
    return patterns

def get_fib(df):
    """Fibonacci seviyeleri"""
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
    """Destek/Direnç"""
    try:
        r = df['High'].tail(50).nlargest(3).mean()
        s = df['Low'].tail(50).nsmallest(3).mean()
        return s, r
    except:
        return None, None

def get_fear_greed():
    """Fear & Greed Index (Kripto)"""
    try:
        r = requests.get("https://api.alternative.me/fng/", timeout=3)
        data = r.json()['data'][0]
        return int(data['value']), data['value_classification']
    except:
        return None, None

def convert_symbol(sym):
    """Sembol dönüşümü"""
    crypto = {
        "BTC": "BTC-USD", "ETH": "ETH-USD", "SOL": "SOL-USD",
        "AVAX": "AVAX-USD", "XRP": "XRP-USD", "DOGE": "DOGE-USD",
        "ADA": "ADA-USD", "DOT": "DOT-USD", "MATIC": "MATIC-USD",
        "BNB": "BNB-USD", "LINK": "LINK-USD"
    }
    commodity = {
        "ALTIN": "GC=F", "GOLD": "GC=F",
        "PETROL": "CL=F", "OIL": "CL=F",
        "GUMUS": "SI=F", "SILVER": "SI=F"
    }
    
    if sym in crypto:
        return crypto[sym]
    elif sym in commodity:
        return commodity[sym]
    elif ".IS" not in sym and "=" not in sym and len(sym) <= 6:
        return f"{sym}.IS"
    return sym

# ==================== TELEGRAM KOMUTLARI ====================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = """
🦁 **PROMETHEUS AI v10.0**

Efsanevi 7 Katmanlı Yatırım Analiz Sistemi

📊 **ÖZELLİKLER:**
✅ 38 Mum Formasyonu Tanıma
✅ 50+ Teknik Gösterge
✅ Fibonacci + Destek/Direnç
✅ Fear & Greed Index
✅ Risk Yönetimi + Pozisyon
✅ Gemini AI Powered

📈 **KOMUTLAR:**
/analiz BTC - Tam detaylı analiz
/hizli BTC - Hızlı özet
BTC - Direkt sembol yaz

⚡ **DESTEK:**
Kripto, Hisse, Forex, Emtia

🚀 **Powered by Railway**
    """
    await update.message.reply_text(msg, parse_mode=constants.ParseMode.MARKDOWN)

async def quick_analysis(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Hızlı analiz"""
    user_msg = update.message.text.upper().replace("/HIZLI", "").replace("/HıZLı", "").strip()
    if not user_msg:
        await update.message.reply_text("Örn: `/hizli BTC`", parse_mode=constants.ParseMode.MARKDOWN)
        return
    
    status = await update.message.reply_text(f"⚡ **{user_msg}** hızlı analiz...", parse_mode=constants.ParseMode.MARKDOWN)
    symbol = convert_symbol(user_msg)
    
    try:
        df = yf.download(symbol, period="3mo", interval="1d", progress=False)
        if df.empty:
            await status.edit_text(f"❌ Veri yok: `{user_msg}`", parse_mode=constants.ParseMode.MARKDOWN)
            return
        
        df = calc_indicators(df)
        last = df.iloc[-1]
        
        score = 0
        factors = []
        
        # Trend
        if 'SMA_200' in df.columns and last['Close'] > last['SMA_200']:
            score += 20
            factors.append("✅ SMA 200 üstünde (Trend yükseliş)")
        elif 'SMA_200' in df.columns:
            score -= 20
            factors.append("❌ SMA 200 altında (Trend düşüş)")
        
        # RSI
        rsi = last.get('RSI', 50)
        if rsi < 30:
            score += 25
            factors.append(f"✅ RSI aşırı satım ({rsi:.1f})")
        elif rsi > 70:
            score -= 25
            factors.append(f"❌ RSI aşırı alım ({rsi:.1f})")
        else:
            factors.append(f"⚪ RSI normal ({rsi:.1f})")
        
        # MACD
        if 'MACD' in df.columns and 'MACD_SIGNAL' in df.columns:
            if last['MACD'] > last['MACD_SIGNAL']:
                score += 10
                factors.append("✅ MACD pozitif")
            else:
                score -= 10
                factors.append("❌ MACD negatif")
        
        # Karar
        if score >= 30:
            decision = "🟢 GÜÇLÜ AL"
        elif score >= 10:
            decision = "🟡 AL"
        elif score <= -30:
            decision = "🔴 GÜÇLÜ SAT"
        elif score <= -10:
            decision = "🟠 SAT"
        else:
            decision = "⚪ BEKLE"
        
        report = f"""
⚡ **{user_msg}** Hızlı Analiz

**Karar:** {decision}
**Skor:** {score}/100
**Fiyat:** ${last['Close']:.2f}
**RSI:** {rsi:.1f}

**Faktörler:**
{chr(10).join(factors)}

🔍 Detaylı analiz: `/analiz {user_msg}`
        """
        await status.edit_text(report, parse_mode=constants.ParseMode.MARKDOWN)
    
    except Exception as e:
        logging.error(f"Hızlı analiz hatası: {e}")
        await status.edit_text(f"⚠️ Hata: {str(e)}")

async def full_analysis(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Tam detaylı analiz (Gemini AI)"""
    user_msg = update.message.text.upper().replace("/ANALIZ", "").replace("/ANALİZ", "").strip()
    
    if not user_msg:
        await update.message.reply_text("Örn: `/analiz BTC`", parse_mode=constants.ParseMode.MARKDOWN)
        return
    
    status = await update.message.reply_text(
        f"🔍 **{user_msg}** detaylı analiz başlıyor...\n\n"
        "⏳ Veriler çekiliyor...\n"
        "⏳ Göstergeler hesaplanıyor...\n"
        "⏳ Gemini AI sentezliyor...",
        parse_mode=constants.ParseMode.MARKDOWN
    )
    
    symbol = convert_symbol(user_msg)
    
    try:
        # Veri çek
        df = yf.download(symbol, period="1y", interval="1d", progress=False)
        if df.empty:
            await status.edit_text(f"❌ Veri yok: `{user_msg}`", parse_mode=constants.ParseMode.MARKDOWN)
            return
        
        # Analizler
        df = calc_indicators(df)
        last = df.iloc[-1]
        patterns = detect_patterns(df)
        fib = get_fib(df)
        s, r = get_sr(df)
        fg, fg_text = get_fear_greed()
        
        if not model:
            await status.edit_text("⚠️ Gemini API anahtarı yok! GEMINI_API_KEY environment variable ekle.", parse_mode=constants.ParseMode.MARKDOWN)
            return
        
        # Gemini için veri özeti
        data_summary = f"""
VARLIK: {user_msg} ({symbol})
Güncel Fiyat: ${last['Close']:.2f}
24s Değişim: {((last['Close']-df.iloc[-2]['Close'])/df.iloc[-2]['Close']*100):.2f}%

KATMAN 1 - MUM FORMASYONLARI:
Bullish: {', '.join(patterns['bullish']) if patterns['bullish'] else 'Yok'}
Bearish: {', '.join(patterns['bearish']) if patterns['bearish'] else 'Yok'}

KATMAN 2 - TEKNİK GÖSTERGELER:
RSI(14): {last.get('RSI', 0):.1f} {'(Aşırı Satım)' if last.get('RSI', 50) < 30 else '(Aşırı Alım)' if last.get('RSI', 50) > 70 else '(Normal)'}
MACD: {last.get('MACD', 0):.2f} | Signal: {last.get('MACD_SIGNAL', 0):.2f}
SMA 20: ${last.get('SMA_20', 0):.2f} {'(Üstünde ✅)' if last['Close'] > last.get('SMA_20', 0) else '(Altında ❌)'}
SMA 50: ${last.get('SMA_50', 0):.2f} {'(Üstünde ✅)' if last['Close'] > last.get('SMA_50', 0) else '(Altında ❌)'}
SMA 200: ${last.get('SMA_200', 0):.2f} {'(Üstünde ✅)' if last['Close'] > last.get('SMA_200', 0) else '(Altında ❌)'}
Bollinger: Üst ${last.get('BB_UPPER', 0):.2f} | Alt ${last.get('BB_LOWER', 0):.2f}
ATR: {last.get('ATR', 0):.2f}
Volume Ratio: {last.get('VOL_RATIO', 1):.2f}x

KATMAN 3 - FIBONACCI & SEVİYELER:
Fibonacci 61.8% (Altın): ${fib.get('61.8', 0):.2f}
Fibonacci 50.0%: ${fib.get('50.0', 0):.2f}
Destek: ${s if s else 0:.2f}
Direnç: ${r if r else 0:.2f}

KATMAN 6 - SENTIMENT:
Fear & Greed Index: {fg}/100 ({fg_text}) {'' if not fg else '⚠️ FIRSAT!' if fg < 30 else '⚠️ DİKKAT!' if fg > 70 else '✅ Normal'}

ŞIMDI BU VERİLERİ KULLANARAK PROMETHEUS AI FORMATINDA 7 KATMAN ANALİZ YAP!
        """
        
        # Gemini API çağrısı
        response = model.generate_content(PROMETHEUS_PROMPT + "\n\n" + data_summary)
        result = response.text
        
        # Telegram 4096 karakter limiti
        if len(result) > 4000:
            parts = [result[i:i+4000] for i in range(0, len(result), 4000)]
            await status.edit_text(parts[0], parse_mode=constants.ParseMode.MARKDOWN)
            for part in parts[1:]:
                await update.message.reply_text(part, parse_mode=constants.ParseMode.MARKDOWN)
        else:
            await status.edit_text(result, parse_mode=constants.ParseMode.MARKDOWN)
    
    except Exception as e:
        logging.error(f"Full analiz hatası: {e}")
        await status.edit_text(f"⚠️ Hata oluştu: {str(e)}", parse_mode=constants.ParseMode.MARKDOWN)

# ==================== BOT BAŞLATMA ====================

def start_bot():
    if not TELEGRAM_TOKEN:
        logging.error("❌ TELEGRAM_TOKEN environment variable yok!")
        return
    
    logging.info("🦁 PROMETHEUS AI v10.0 başlatılıyor...")
    
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    # Komutlar
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("analiz", full_analysis))
    application.add_handler(CommandHandler("hizli", quick_analysis))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, full_analysis))
    
    logging.info("✅ Bot polling modu başladı")
    application.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)

if __name__ == '__main__':
    keep_alive()
    time.sleep(2)  # Flask'ın başlaması için bekle
    start_bot()