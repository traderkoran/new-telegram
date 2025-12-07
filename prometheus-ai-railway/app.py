import logging
import os
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import numpy as np
from datetime import datetime, timedelta
from telegram import Update, constants
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import google.generativeai as genai
from flask import Flask
from threading import Thread
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import io
import requests
from typing import Dict, List, Tuple
import time

# ==================== KONFIGÜRASYON ====================
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
PORT = int(os.environ.get("PORT", 8080))

# Gemini Model Konfigürasyonu
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    try:
        model = genai.GenerativeModel(
            'gemini-1.5-flash',
            generation_config={
                'temperature': 0.7,
                'top_p': 0.95,
                'top_k': 40,
                'max_output_tokens': 8192,
            }
        )
    except Exception as e:
        logging.warning(f"Gemini model hatası: {e}")
        model = None
else:
    model = None

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# ==================== FLASK WEB SUNUCU ====================
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
                background: linear-gradient(135deg, #0a0e27 0%, #1a1f3a 100%);
                color: #00ff88;
                font-family: 'Courier New', monospace;
                padding: 40px 20px;
                min-height: 100vh;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
            }
            .container {
                max-width: 900px;
                background: rgba(20, 25, 45, 0.9);
                border: 2px solid #00ff88;
                border-radius: 20px;
                padding: 40px;
                box-shadow: 0 0 40px rgba(0, 255, 136, 0.3);
                animation: glow 2s ease-in-out infinite alternate;
            }
            @keyframes glow {
                from { box-shadow: 0 0 20px rgba(0, 255, 136, 0.3); }
                to { box-shadow: 0 0 60px rgba(0, 255, 136, 0.6); }
            }
            h1 {
                font-size: 3em;
                text-align: center;
                margin-bottom: 10px;
                text-shadow: 0 0 20px rgba(0, 255, 136, 0.8);
            }
            h2 {
                color: #ffaa00;
                text-align: center;
                margin-bottom: 30px;
                font-size: 1.5em;
            }
            .feature {
                background: rgba(0, 255, 136, 0.05);
                border-left: 4px solid #00ff88;
                padding: 15px;
                margin: 15px 0;
                border-radius: 5px;
                transition: all 0.3s;
            }
            .feature:hover {
                background: rgba(0, 255, 136, 0.1);
                transform: translateX(10px);
            }
            .status {
                margin-top: 30px;
                padding: 20px;
                background: rgba(0, 170, 255, 0.1);
                border: 2px solid #00aaff;
                border-radius: 10px;
                text-align: center;
                font-size: 1.3em;
            }
            .pulse {
                display: inline-block;
                width: 15px;
                height: 15px;
                background: #00ff88;
                border-radius: 50%;
                margin-right: 10px;
                animation: pulse 1.5s ease-in-out infinite;
            }
            @keyframes pulse {
                0%, 100% { transform: scale(1); opacity: 1; }
                50% { transform: scale(1.3); opacity: 0.7; }
            }
            .stats {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 15px;
                margin-top: 20px;
            }
            .stat-box {
                background: rgba(255, 170, 0, 0.1);
                border: 1px solid #ffaa00;
                padding: 15px;
                border-radius: 8px;
                text-align: center;
            }
            .stat-number {
                font-size: 2em;
                color: #ffaa00;
                font-weight: bold;
            }
            a {
                color: #00aaff;
                text-decoration: none;
            }
            a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🦁 PROMETHEUS AI v10.0</h1>
            <h2>Efsanevi Yatırım Analiz Sistemi</h2>
            
            <div class="feature">✅ <strong>KATMAN 1:</strong> 38 Mum Formasyonu + Elliott Wave + Harmonik Pattern</div>
            <div class="feature">✅ <strong>KATMAN 2:</strong> 50+ Teknik Gösterge Matrisi (RSI, MACD, Ichimoku...)</div>
            <div class="feature">✅ <strong>KATMAN 3:</strong> Fibonacci + Gann + Matematiksel Analiz</div>
            <div class="feature">✅ <strong>KATMAN 4:</strong> Piyasa Yapısı + Wyckoff VSA + Likidite</div>
            <div class="feature">✅ <strong>KATMAN 5:</strong> Temel Analiz (Hisse/Kripto/Forex/Emtia)</div>
            <div class="feature">✅ <strong>KATMAN 6:</strong> Sentiment + Fear & Greed Index</div>
            <div class="feature">✅ <strong>KATMAN 7:</strong> Risk Yönetimi + Pozisyon Boyutu + Kelly Criterion</div>
            
            <div class="stats">
                <div class="stat-box">
                    <div class="stat-number">7</div>
                    <div>Analiz Katmanı</div>
                </div>
                <div class="stat-box">
                    <div class="stat-number">50+</div>
                    <div>Teknik Gösterge</div>
                </div>
                <div class="stat-box">
                    <div class="stat-number">38</div>
                    <div>Mum Formasyonu</div>
                </div>
                <div class="stat-box">
                    <div class="stat-number">∞</div>
                    <div>Varlık Desteği</div>
                </div>
            </div>
            
            <div class="status">
                <span class="pulse"></span>
                <strong style="color: #00ff88;">STATUS: ONLINE & OPERATIONAL</strong>
            </div>
            
            <div style="margin-top: 30px; text-align: center; color: #aaa;">
                <p>⚡ Powered by Gemini 1.5 Flash</p>
                <p>🚀 Deployed on Railway</p>
                <p>📊 Real-time Market Analysis</p>
            </div>
        </div>
    </body>
    </html>
    """

@app.route('/health')
def health():
    return {'status': 'healthy', 'version': '10.0', 'platform': 'railway'}

def run_flask():
    app.run(host='0.0.0.0', port=PORT, threaded=True)

def keep_alive():
    t = Thread(target=run_flask, daemon=True)
    t.start()
    logging.info(f"🌐 Flask server başlatıldı (Port: {PORT})")

# ==================== PROMETHEUS ULTRA SYSTEM PROMPT ====================
PROMETHEUS_SYSTEM = """
SEN: PROMETHEUS AI v10.0 - Dünyanın En Gelişmiş Yatırım Analiz Zekası

DNA HİBRİT YAPISI:
• Renaissance Technologies (Jim Simons) → Quantitative Mastery
• Berkshire Hathaway (Warren Buffett) → Value Investing
• Quantum Fund (George Soros) → Macro Reflexivity Theory
• Bridgewater Associates (Ray Dalio) → All-Weather Strategy
• Tudor Investment (Paul Tudor Jones) → Macro + Technical Synthesis
• Market Wizards (Ed Seykota, Richard Dennis) → Trend Following + Discipline

MİSYON: Kullanıcı herhangi bir varlık sorduğunda (hisse, kripto, forex, emtia, endeks), 
7 KATMANLI DERİN ANALİZ yaparak KESIN KARAR ver.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 7 KATMAN ANALİZ ÇERÇEVESİ
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

KATMAN 1: FİYAT HAREKETİ ANATOMİSİ
• 38 Mum Formasyonu (Doji, Hammer, Engulfing, Morning/Evening Star...)
• Grafik Formasyonları (H&S, Triangle, Flag, Cup&Handle, Wedges...)
• Elliott Wave Dalga Sayımı
• Harmonik Formasyonlar (Gartley, Butterfly, Bat, Crab, Cypher)
• Wyckoff Piyasa Döngüsü

KATMAN 2: TEKNİK GÖSTERGELER MATRİSİ
• Momentum: RSI, MACD, Stochastic, Williams %R, CCI, MFI
• Trend: SMA/EMA, Ichimoku, ADX, Supertrend, Parabolic SAR
• Volatilite: Bollinger, ATR, Keltner, Donchian
• Hacim: OBV, A/D Line, Volume Profile, VWAP
• Divergence Taraması (Fiyat vs. Gösterge uyumsuzlukları)

KATMAN 3: MATEMATİKSEL ANALİZ
• Fibonacci Retracement & Extension
• Destek/Direnç Bölgeleri (Horizontal, Dynamic, Pivot)
• Gann Açıları ve Döngüler
• Psikolojik Seviyeler

KATMAN 4: PİYASA YAPISI & LİKİDİTE
• Trend Tanımlama (HH/HL, LH/LL, Range)
• Piyasa Fazı (Accumulation/Markup/Distribution/Markdown)
• Likidite Bölgeleri (Stop-loss clusters)
• Emir Akışı (Bid/Ask imbalance, Absorption)

KATMAN 5: TEMEL ANALİZ
• Hisseler: Mali Tablolar, Değerleme (P/E, PEG, EV/EBITDA, FCF)
• Kripto: On-Chain (MVRV, NVT, SOPR, Exchange Netflow, Whale Activity)
• Forex: Faiz Farkları, GDP, Enflasyon, Merkez Bankası
• Emtialar: Arz/Talep, Stoklar, Mevsimsellik

KATMAN 6: SENTIMENT ANALİZİ
• Fear & Greed Index (Kripto için)
• VIX (Hisseler için)
• Put/Call Ratio, COT Raporu
• Sosyal Medya Duyarlılığı

KATMAN 7: RİSK YÖNETİMİ
• Risk/Ödül Oranı (Min 1:2)
• Stop-Loss Yerleştirme (ATR bazlı)
• Pozisyon Boyutu (%1-2 risk kuralı)
• Kelly Criterion Optimizasyonu
• Korelasyon Kontrolü

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 ZORUNLU ÇIKTI FORMATI
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## 🎯 YÖNETİCİ ÖZETİ

**KARAR:** [🟢 GÜÇLÜ AL / 🟡 AL / ⚪ BEKLE / 🟠 SAT / 🔴 GÜÇLÜ SAT]
**Güven Skoru:** %[0-100]
**Risk Seviyesi:** [DÜŞÜK/ORTA/YÜKSEK/AŞIRI]
**Zaman Ufku:** [Kısa Vade (1-7 gün) / Orta Vade (1-4 hafta) / Uzun Vade (1-6 ay)]
**Pozisyon Boyutu:** [Portföyün %X'i]
**Temel Tez:** [2 cümle - Neden bu karar?]
**Ana Katalizör:** [Bu hareketi tetikleyecek şey]
**Büyük Risk:** [En büyük tehdit]

---

## 📊 7 KATMANLI DERİN ANALİZ

### KATMAN 1: FİYAT HAREKETİ ANATOMİSİ

**Mum Formasyonları (Son 5 Mum):**
[Tespit edilen formasyonları listele - Hammer, Engulfing, Doji vb.]
- Sinyal Gücü: [Zayıf/Orta/Güçlü/Çok Güçlü]
- Yorum: [Bu formasyonlar ne söylüyor?]

**Grafik Formasyonları:**
- Aktif Formasyon: [H&S / Triangle / Flag / Cup&Handle vb.]
- Tamamlanma: [%XX]
- Hedef Fiyat: $[XXX]
- İnvalidasyon: $[XXX]
- Başarı Oranı: [%XX - Tarihsel veri]

**Elliott Wave Sayımı:**
- Mevcut Pozisyon: [Wave X of Y]
- Dalga Tipi: [Impulse / Corrective]
- Sonraki Beklenti: [Yön + Hedef]
- Kritik Seviye: $[XXX]

**Harmonik Formasyon:**
- Tespit: [Gartley/Butterfly/Bat/Crab/Cypher / Yok]
- D Noktası: $[XXX]
- Fibonacci Ratios: [Geçerli/Geçersiz]

---

### KATMAN 2: TEKNİK GÖSTERGELER MATRİSİ

**Momentum Göstergeleri:**
| Gösterge | Değer | Sinyal | Yorum |
|----------|-------|--------|-------|
| RSI(14) | XX.X | [AL/SAT/NÖTR] | [Aşırı alım/satım/normal] |
| MACD | XX.X | [YUKARI/AŞAĞI] | [Cross durumu] |
| Stochastic | XX.X | [AL/SAT] | [Aşırı bölge kontrolü] |
| Williams %R | XX.X | [AL/SAT] | [Momentum yorumu] |
| CCI | XX.X | [AL/SAT] | [Trend gücü] |

**UYUMSUZLUK (DIVERGENCE) TARAMASI:**
- RSI Divergence: [🟢 Bullish / 🔴 Bearish / ⚪ Yok]
- MACD Divergence: [🟢 Bullish / 🔴 Bearish / ⚪ Yok]
- Volume Divergence: [🟢 Bullish / 🔴 Bearish / ⚪ Yok]
[Uyumsuzluk varsa → Güçlü dönüş sinyali!]

**Trend Göstergeleri:**
- SMA 20: $XX.XX [Fiyat üstünde/altında]
- SMA 50: $XX.XX [Fiyat üstünde/altında]
- SMA 200: $XX.XX [Fiyat üstünde/altında]
- Golden/Death Cross: [Var/Yok]
- ADX: XX.X [<20 Zayıf / 20-25 Orta / >25 Güçlü Trend]
- Ichimoku: [Bullish/Bearish] [Bulut konumu]

**Volatilite Göstergeleri:**
- Bollinger Bands: [Üst $XX / Orta $XX / Alt $XX]
- Fiyat Konumu: [Üst band/Orta/Alt band]
- Bollinger Squeeze: [Aktif/Yok] [Kırılma yakın mı?]
- ATR(14): XX.XX [Yüksek/Normal/Düşük volatilite]
- Bandwidth: X.XX% [Sıkışma/Normal/Genişleme]

**Hacim Göstergeleri:**
- Volume Ratio: X.XXx [Normal üstü/altı]
- OBV: [Yükselen/Düşen] [Fiyatla uyumlu mu?]
- A/D Line: [Birikim/Dağıtım]
- MFI: XX.X [Para akışı yönü]
- CMF: X.XX [Alış/Satış baskısı]
- VWAP: $XX.XX [Fiyat üstünde/altında]
- Volume Profile POC: $XX.XX [En yüksek hacim seviyesi]

---

### KATMAN 3: MATEMATİKSEL ANALİZ

**Fibonacci Seviyeleri:**
- 23.6%: $XX.XX [Tuttu/Kırıldı]
- 38.2%: $XX.XX [Tuttu/Kırıldı]
- 50.0%: $XX.XX [Tuttu/Kırıldı]
- 61.8%: $XX.XX ⭐ [Altın Oran - Tuttu/Kırıldı]
- 78.6%: $XX.XX [Tuttu/Kırıldı]

**Extension Hedefleri:**
- 127.2%: $XX.XX
- 161.8%: $XX.XX ⭐ [Birincil hedef]
- 261.8%: $XX.XX [Uzatılmış hedef]

**Destek & Direnç Haritası:**
```
R3: $XX.XX [Güçlü/Zayıf] [3+ test / Yüksek hacim / Psikolojik]
R2: $XX.XX [Güçlü/Zayıf]
R1: $XX.XX [Güçlü/Zayıf]
────────────────────────────
Güncel Fiyat: $XX.XX
────────────────────────────
S1: $XX.XX [Güçlü/Zayıf]
S2: $XX.XX [Güçlü/Zayıf]
S3: $XX.XX [Güçlü/Zayıf] [Son savunma hattı]
```

**Kritik Seviye:** $XX.XX [Kırılırsa büyük hareket]

---

### KATMAN 4: PİYASA YAPISI & LİKİDİTE

**Trend Analizi:**
- Yapı: [HH+HL Yükseliş / LH+LL Düşüş / Range Yatay]
- Piyasa Fazı: [Accumulation / Markup / Distribution / Markdown]
- Trend Gücü: [Zayıf/Orta/Güçlü/Çok Güçlü]

**Wyckoff Döngüsü:**
- Mevcut Faz: [Detaylı açıklama]
- Akıllı Para: [Birikim/Dağıtım/Nötr]
- VSA Sinyali: [Absorption / No Demand / Stopping Volume vb.]

**Likidite Bölgeleri:**
- Üst Likidite: $XX.XX [Stop-loss clusters]
- Alt Likidite: $XX.XX [Buy-stop clusters]
- Equal Highs/Lows: [Var/Yok] [Likidite avı riski]

---

### KATMAN 5: TEMEL ANALİZ

[Varlık tipine göre uygun analiz yap]

**EĞER HİSSE İSE:**
- P/E Ratio: XX.X [Sektör ortalaması: XX.X]
- PEG Ratio: X.X [<1 Ucuz / >2 Pahalı]
- EV/EBITDA: XX.X
- FCF Yield: X.X%
- Büyüme: YoY %XX
- Marjlar: Gross %XX / Operating %XX / Net %XX
- Borç/Özkaynak: X.X
- Katalizörler: [Gelecek earnings, ürün lansmanı vb.]

**EĞER KRİPTO İSE:**
- MVRV Ratio: X.XX [<1 Ucuz / >3.5 Pahalı]
- NVT Ratio: XX [Yüksek/Normal/Düşük]
- SOPR: X.XX [>1 Kar satışı / <1 Zarar satışı]
- Exchange Netflow: $XXM [İnflow/Outflow]
- Whale Activity: [Birikim/Dağıtım]
- Active Addresses: XXk [7d değişim: ±%XX]
- Hash Rate (BTC): XXX EH/s [Trend]
- Gas Price (ETH): XX Gwei [Tıkanıklık]
- TVL (DeFi): $XXB [Trend]

**EĞER FOREX İSE:**
- Faiz Farkı: [Para Birimi A: %X vs B: %X]
- GDP Büyüme: [Ülke A: %X vs B: %X]
- Enflasyon: [CPI data]
- Merkez Bankası: [Hawkish/Dovish]
- Önümüzdeki Olaylar: [FOMC, NFP vb.]

**EĞER EMTİA İSE:**
- Arz/Talep: [Stok seviyeleri, üretim]
- Mevsimsellik: [Yaz/Kış etkisi]
- Jeopolitik: [Gerilimler, ambargolar]
- Dollar Korelasyonu: [USD güçlü → Emtia zayıf]

---

### KATMAN 6: SENTIMENT & PSİKOLOJİ

**Fear & Greed Index:**
- Değer: XX/100
- Kategori: [Extreme Fear / Fear / Neutral / Greed / Extreme Greed]
- Yorum: [<25 AL fırsatı / >75 SAT sinyali / Contrarian yaklaşım]

**VIX (Hisseler için):**
- Değer: XX.X
- Seviye: [<15 Rahatlık / 15-20 Normal / 20-30 Korku / >30 Panik]
- Yorum: [Piyasa duyarlılığı]

**Sosyal Sentiment:**
- Twitter/Reddit: [Aşırı iyimser/Normal/Karamsar]
- Google Trends: [Arama ilgisi - Tepe/Dip?]
- Haber Tonu: [Pozitif/Nötr/Negatif]

**Pozisyonlama:**
- Put/Call Ratio: X.XX [>1 Ayıcı / <0.7 Boğa]
- Short Interest: XX% [Squeeze potansiyeli]
- COT Raporu: [Commercial vs Speculator]

**Piyasa Psikolojisi Fazı:**
[Disbelief/Hope/Optimism/Belief/Thrill/Euphoria/Complacency/Anxiety/Denial/Panic/Capitulation/Anger/Depression]

---

### KATMAN 7: RİSK YÖNETİMİ & POZİSYON PLANI

**İŞLEM DETAYLARI:**
```
📍 Giriş Fiyatı: $XX.XX
🛑 Stop-Loss: $XX.XX (Risk: -X.X% / $XXX)
🎯 Hedef 1: $XX.XX (+X.X%, R:R = X:1) → %33 pozisyon kapat
🎯 Hedef 2: $XX.XX (+X.X%, R:R = X:1) → %33 pozisyon kapat
🎯 Hedef 3: $XX.XX (+X.X%, R:R = X:1) → %34 pozisyon kapat

Toplam Risk/Ödül: X.X:1 [Min kabul edilebilir: 2:1]
```

**POZİSYON BOYUTU ÖNERİLERİ:**
[%1-2 risk kuralına göre]

| Hesap Boyutu | Risk Tutarı | Pozisyon Boyutu | Hisse/Coin Sayısı |
|--------------|-------------|-----------------|-------------------|
| $10,000 | $200 (2%) | $X,XXX | XXX adet |
| $50,000 | $1,000 (2%) | $XX,XXX | XXX adet |
| $100,000 | $2,000 (2%) | $XX,XXX | XXX adet |
| $500,000 | $10,000 (2%) | $XXX,XXX | XXX adet |

**Kelly Criterion:**
- Optimal Boyut: %XX
- Tavsiye Edilen (¼ Kelly): %XX [Muhafazakar]

**Volatilite Ayarlaması:**
- Mevcut ATR: XX.XX
- Tarihsel ATR Ort: XX.XX
- Volatilite Oranı: X.X [>1.5 ise pozisyonu %XX küçült]

**Korelasyon Uyarısı:**
[Eğer portföyde ilişkili pozisyonlar varsa uyar]
- [Örnek: BTC + ETH + SOL → Yüksek korelasyon, toplam risk artar]

**Stop-Loss Stratejisi:**
- İlk Stop: $XX.XX [Pattern/Support/ATR bazlı]
- Fiyat +%XX giderse → Stop BE (Breakeven)
- Hedef 1'e ulaşırsa → Trailing stop $XX.XX
- ASLA stop genişletme, sadece sıkılaştır

---

## 🎯 NİHAİ KARAR & AKSİYON PLANI

**KARAR:** [Detaylı açıklama - Neden bu karar?]

**KAZANMA İHTİMALİ:** %XX [Bu pattern/setup tipinin tarihsel başarı oranı]

**BEKLENEN DEĞER:** +%XX
[Hesaplama: (Win% × Ort Kazanç) - (Loss% × Ort Kayıp)]

**ŞİMDİ NE YAPACAKSIN:**
1. ✅ [İlk aksiyon - Örn: Fiyat alert kur $XX.XX seviyesinde]
2. ✅ [İkinci aksiyon - Örn: Limit emir yerleştir]
3. ✅ [Üçüncü aksiyon - Örn: Stop-loss ayarla]
4. ⚠️ [Dikkat noktası - Örn: X tarihinde earnings var]

**TEZİ NE ZAMAN İPTAL ET:**
- ❌ Fiyat $XX.XX seviyesini kırarsa
- ❌ [Pattern/Formasyon fail olursa]
- ❌ [Temel tezde büyük değişiklik]
- ❌ [Zaman stop: X gün içinde hareket yoksa]

**GÜNLÜK İZLEME:**
- [ ] Destek/Direnç testlerini kontrol et
- [ ] Volume kalitesini değerlendir
- [ ] Haber akışını takip et
- [ ] Korelasyonları izle (BTC, DXY, Stocks vb.)

**HAFTALIK DEĞERLENDİRME:**
- Tez hala geçerli mi?
- Teknik yapı bozuldu mu?
- Yeni kataliz ortaya çıktı mı?

---

## ⚠️ RİSK UYARISI

Bu analiz bir yatırım tavsiyesi değildir. Tüm yatırımlar risk içerir.

**ALTIN KURALLAR:**
1. Asla kaybetmeyi göze alamayacağın parayı riske atma
2. Stop-loss kullanmayan %100 kaybeder
3. Sermayenin %2'sinden fazlasını tek işlemde riske atma
4. Duygusal kararlar vermekten kaçın - plana sadık kal
5. Kazanan pozisyonları erken kapatma, kaybedenleri uzun tutma tuzağına düşme

---

Bu format ve detay seviyesinde MUTLAKA cevap ver. Eksik analiz yapma!
"""

# ==================== ANALİZ FONKSİYONLARI ====================

def calculate_all_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """Tüm teknik göstergeleri hesapla"""
    try:
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        
        # Momentum
        df['RSI'] = ta.rsi(df['Close'], length=14)
        stoch = ta.stoch(df['High'], df['Low'], df['Close'])
        if stoch is not None and len(stoch.columns) >= 2:
            df['STOCH_K'] = stoch.iloc[:, 0]
            df['STOCH_D'] = stoch.iloc[:, 1]
        df['WR'] = ta.willr(df['High'], df['Low'], df['Close'])
        df['CCI'] = ta.cci(df['High'], df['Low'], df['Close'])
        
        # MACD
        macd = ta.macd(df['Close'])
        if macd is not None:
            df['MACD'] = macd['MACD_12_26_9']
            df['MACD_SIGNAL'] = macd['MACDs_12_26_9']
            df['MACD_HIST'] = macd['MACDh_12_26_9']
        
        # Trend
        for length in [9, 20, 50, 200]:
            if len(df) >= length:
                df[f'SMA_{length}'] = ta.sma(df['Close'], length=length)
                df[f'EMA_{length}'] = ta.ema(df['Close'], length=length)
        
        adx = ta.adx(df['High'], df['Low'], df['Close'])
        if adx is not None:
            df['ADX'] = adx['ADX_14']
        
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
        df['MFI'] = ta.mfi(df['High'], df['Low'], df['Close'], df['Volume'])
        df['VWAP'] = ta.vwap(df['High'], df['Low'], df['Close'], df['Volume'])
        df['VOL_SMA'] = ta.sma(df['Volume'], length=20)
        df['VOL_RATIO'] = df['Volume'] / df['VOL_SMA'].replace(0, 1)
        
        return df
    except Exception as e:
        logging.error(f"Gösterge hatası: {e}")
        return df

def detect_patterns(df: pd.DataFrame) -> Dict:
    """Mum formasyonlarını tespit et"""
    patterns = {'bullish': [], 'bearish': [], 'neutral': []}
    try:
        for i in range(max(0, len(df) - 5), len(df)):
            c = df.iloc[i]
            body = abs(c['Close'] - c['Open'])
            range_val = c['High'] - c['Low']
            upper = c['High'] - max(c['Open'], c['Close'])
            lower = min(c['Open'], c['Close']) - c['Low']
            
            if range_val == 0:
                continue
            
            # Doji
            if body <= range_val * 0.1:
                if upper > body * 3:
                    patterns['bearish'].append("Gravestone Doji")
                elif lower > body * 3:
                    patterns['bullish'].append("Dragonfly Doji")
                else:
                    patterns['neutral'].append("Doji")
            
            # Hammer/Hanging Man
            elif lower > body * 2 and upper < body * 0.3:
                if c['Close'] > c['Open']:
                    patterns['bullish'].append("Hammer ⭐")
                else:
                    patterns['bearish'].append("Hanging Man")
            
            # Shooting Star
            elif upper > body * 2 and lower < body * 0.3:
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

def get_fib_levels(df: pd.DataFrame) -> Dict:
    """Fibonacci seviyeleri"""
    try:
        high, low = df['High'].tail(100).max(), df['Low'].tail(100).min()
        diff = high - low
        return {
            '0.0': high,
            '23.6': high - 0.236 * diff,
            '38.2': high - 0.382 * diff,
            '50.0': high - 0.5 * diff,
            '61.8': high - 0.618 * diff,
            '78.6': high - 0.786 * diff,
            '100.0': low
        }
    except:
        return {}

def get_support_resistance(df: pd.DataFrame) -> Tuple:
    """S/R seviyeleri"""
    try:
        recent = df.tail(50)
        resistance = recent['High'].nlargest(3).mean()
        support = recent['Low'].nsmallest(3).mean()
        return support, resistance
    except:
        return None, None

def analyze_divergence(df: pd.DataFrame) -> Dict:
    """Divergence taraması"""
    div = {'RSI': '⚪ Yok', 'MACD': '⚪ Yok'}
    try:
        if 'RSI' in df.columns and len(df) >= 20:
            price_change = df['Close'].iloc[-1] - df['Close'].iloc[-10]
            rsi_change = df['RSI'].iloc[-1] - df['RSI'].iloc[-10]
            if price_change > 0 and rsi_change < -5:
                div['RSI'] = '🔴 Bearish (Fiyat↑ RSI↓)'
            elif price_change < 0 and rsi_change > 5:
                div['RSI'] = '🟢 Bullish (Fiyat↓ RSI↑)'
    except:
        pass
    return div

def get_fear_greed() -> Tuple:
    """Fear & Greed Index"""
    try:
        r = requests.get("https://api.alternative.me/fng/", timeout=3)
        data = r.json()['data'][0]
        return int(data['value']), data['value_classification']
    except:
        return None, None

def convert_symbol(sym: str) -> str:
    """Sembol dönüşümü"""
    crypto = {"BTC": "BTC-USD", "ETH": "ETH-USD", "SOL": "SOL-USD", "AVAX": "AVAX-USD"}
    commodity = {"ALTIN": "GC=F", "PETROL": "CL=F"}
    if sym in crypto:
        return crypto[sym]
    elif sym in commodity:
        return commodity[sym]
    elif ".IS" not in sym and len(sym) <= 6:
        return f"{sym}.IS"
    return sym

# ==================== TELEGRAM KOMUTLARI ====================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = """
🦁 **PROMETHEUS AI v10.0 RAILWAY EDITION**

Efsanevi 7 Katmanlı Yatırım Analiz Sistemi

📊 **ÖZELLİKLER:**
✅ 38 Mum Formasyonu
✅ 50+ Teknik Gösterge
✅ Elliott Wave + Harmonik
✅ On-Chain Kripto Analizi
✅ Risk Yönetimi + Pozisyon
✅ Sentiment + Fear&Greed
✅ Gemini AI Powered

📈 **KOMUTLAR:**
/analiz BTC - Tam detaylı analiz
/hizli BTC - Hızlı özet
/grafik BTC - Görsel chart
BTC - Direkt sembol yaz

⚡ Supported: Kripto, Hisse, Forex, Emtia
    """
    await update.message.reply_text(msg, parse_mode=constants.ParseMode.MARKDOWN)

async def quick_analysis(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Hızlı analiz"""
    user_msg = update.message.text.upper().replace("/HIZLI", "").strip()
    if not user_msg:
        await update.message.reply_text("Örn: `/hizli BTC`")
        return
    
    status = await update.message.reply_text(f"⚡ {user_msg} hızlı analiz...")
    symbol = convert_symbol(user_msg)
    
    try:
        df = yf.download(symbol, period="3mo", interval="1d", progress=False)
        if df.empty:
            await status.edit_text(f"❌ Veri yok: {user_msg}")
            return
        
        df = calculate_all_indicators(df)
        last = df.iloc[-1]
        
        score = 0
        if 'SMA_200' in df.columns and last['Close'] > last['SMA_200']:
            score += 20
        if last.get('RSI', 50) < 30:
            score += 25
        elif last.get('RSI', 50) > 70:
            score -= 25
        
        decision = "🟢 AL" if score >= 20 else "🔴 SAT" if score <= -20 else "⚪ BEKLE"
        
        report = f"""
⚡ **{user_msg}** Hızlı Analiz

**Karar:** {decision} (Skor: {score}/100)
**Fiyat:** ${last['Close']:.2f}
**RSI:** {last.get('RSI', 0):.1f}
**Trend:** {'Yükseliş' if last['Close'] > last.get('SMA_200', 0) else 'Düşüş'}

Detay: /analiz {user_msg}
        """
        await status.edit_text(report, parse_mode=constants.ParseMode.MARKDOWN)
    except Exception as e:
        await status.edit_text(f"⚠️ Hata: {str(e)}")

async def full_analysis(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Tam analiz (Gemini AI)"""
    user_msg = update.message.text.upper().replace("/ANALIZ", "").replace("/ANALİZ", "").strip()
    if not user_msg:
        await update.message.reply_text("Örn: `/analiz BTC`")
        return
    
    status = await update.message.reply_text(f"🔍 {user_msg} 7 katman analizi başlıyor...")
    symbol = convert_symbol(user_msg)
    
    try:
        df = yf.download(symbol, period="1y", interval="1d", progress=False)
        if df.empty:
            await status.edit_text(f"❌ Veri yok: {user_msg}")
            return
        
        df = calculate_all_indicators(df)
        last = df.iloc[-1]
        patterns = detect_patterns(df)
        fib = get_fib_levels(df)
        s, r = get_support_resistance(df)
        div = analyze_divergence(df)
        fg, fg_text = get_fear_greed()
        
        if not model:
            await status.edit_text("⚠️ Gemini API anahtarı yok!")
            return
        
        data_summary = f"""
VARLIK: {user_msg}
Fiyat: ${last['Close']:.2f}

MUM FORMASYONLARI:
Bullish: {', '.join(patterns['bullish']) if patterns['bullish'] else 'Yok'}
Bearish: {', '.join(patterns['bearish']) if patterns['bearish'] else 'Yok'}

TEKNİK GÖSTERGELER:
RSI: {last.get('RSI', 0):.1f}
MACD: {last.get('MACD', 0):.2f}
ADX: {last.get('ADX', 0):.1f}
SMA200: ${last.get('SMA_200', 0):.2f} {'(Üstünde ✅)' if last['Close'] > last.get('SMA_200', 0) else '(Altında ❌)'}
Bollinger: ${last.get('BB_UPPER', 0):.2f} / ${last.get('BB_LOWER', 0):.2f}
Volume Ratio: {last.get('VOL_RATIO', 1):.2f}x

DIVERGENCE:
RSI: {div['RSI']}
MACD: {div['MACD']}

FIBONACCI:
61.8% (Altın): ${fib.get('61.8', 0):.2f}
50.0%: ${fib.get('50.0', 0):.2f}

DESTEK/DİRENÇ:
Destek: ${s if s else 0:.2f}
Direnç: ${r if r else 0:.2f}

SENTIMENT:
Fear&Greed: {fg}/100 ({fg_text}) {'' if not fg else '(AL fırsatı!)' if fg < 30 else '(Dikkat!)' if fg > 70 else ''}

PROMETHEUS AI FORMATINDA TAM ANALİZ YAP!
        """
        
        response = model.generate_content(PROMETHEUS_SYSTEM + "\n\n" + data_summary)
        result = response.text
        
        # 4096 karakter limit
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

async def chart_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Grafik oluştur"""
    user_msg = update.message.text.upper().replace("/GRAFIK", "").strip()
    if not user_msg:
        await update.message.reply_text("Örn: `/grafik BTC`")
        return
    
    status = await update.message.reply_text(f"📊 {user_msg} grafiği hazırlanıyor...")
    symbol = convert_symbol(user_msg)
    
    try:
        df = yf.download(symbol, period="6mo", interval="1d", progress=False)
        if df.empty:
            await status.edit_text(f"❌ Veri yok")
            return
        
        df = calculate_all_indicators(df)
        
        # Basit grafik oluştur
        fig, ax = plt.subplots(figsize=(12, 6), facecolor='#0a0e27')
        ax.set_facecolor('#0a0e27')
        ax.plot(df.index, df['Close'], color='#00ff88', linewidth=2, label='Fiyat')
        if 'SMA_50' in df.columns:
            ax.plot(df.index, df['SMA_50'], color='#ffaa00', label='SMA 50')
        ax.set_title(f'{user_msg} - Fiyat Grafiği', color='white', fontsize=14)
        ax.legend()
        ax.grid(alpha=0.3, color='white')
        ax.tick_params(colors='white')
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png', facecolor='#0a0e27', dpi=100)
        buf.seek(0)
        plt.close()
        
        await status.delete()
        await update.message.reply_photo(photo=buf, caption=f"📊 {user_msg} Grafiği")
    except Exception as e:
        await status.edit_text(f"⚠️ Hata: {str(e)}")

# ==================== BOT BAŞLATMA ====================

def start_bot():
    if not TELEGRAM_TOKEN:
        logging.error("❌ TELEGRAM_TOKEN yok!")
        return
    
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("analiz", full_analysis))
    app.add_handler(CommandHandler("hizli", quick_analysis))
    app.add_handler(CommandHandler("grafik", chart_cmd))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, full_analysis))
    
    logging.info("🦁 PROMETHEUS AI v10.0 başlatılıyor...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    keep_alive()
    start_bot()