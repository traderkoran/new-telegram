# 🦁 PROMETHEUS AI v10.0 - Railway Edition

## Efsanevi 7 Katmanlı Yatırım Analiz Sistemi

### ✨ Özellikler
- ✅ 38 Mum Formasyonu Tanıma
- ✅ 50+ Teknik Gösterge (RSI, MACD, Bollinger...)
- ✅ Fibonacci Retracement & Extension
- ✅ Destek/Direnç Analizi
- ✅ Fear & Greed Index (Kripto için)
- ✅ Risk Yönetimi + Pozisyon Hesaplama
- ✅ Gemini 1.5 Flash AI Powered
- ✅ %100 Ücretsiz (Railway 500 saat/ay)

---

## 🚀 Railway Deploy (3 Dakika)

### 1. GitHub Repo Oluştur

```bash
# Yeni klasör
mkdir prometheus-railway
cd prometheus-railway

# Dosyaları kopyala (5 dosya: app.py, requirements.txt, Dockerfile, .gitignore, README.md)

# Git
git init
git add .
git commit -m "PROMETHEUS AI v10.0"

# GitHub'a push
git remote add origin https://github.com/KULLANICI_ADIN/prometheus-railway.git
git branch -M main
git push -u origin main
```

### 2. Railway Deploy

1. **https://railway.app** → Login (GitHub ile)
2. **New Project** → **Deploy from GitHub repo**
3. Repo seç: `prometheus-railway`
4. Railway otomatik Dockerfile bulacak ✅

### 3. Environment Variables Ekle

Railway Dashboard → Projen → **Variables** sekmesi

**ZORUNLU:**
```
TELEGRAM_TOKEN = 6123456789:AAHxxxxxxxxxxxxxxxxxxxxxxx
GEMINI_API_KEY = AIzaSyxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**Nasıl Alınır?**

**TELEGRAM_TOKEN:**
- Telegram → `@BotFather`
- `/newbot` → Bot adı ver
- Token'ı kopyala

**GEMINI_API_KEY:**
- https://ai.google.dev
- "Get API Key" → Create
- Key'i kopyala

### 4. Deploy!

Railway otomatik deploy edecek. **Deployments** → Logs'ta:

```
✅ Building with Dockerfile...
✅ Installing dependencies...
✅ Successfully built
✅ Flask server başlatıldı
✅ Bot polling modu başladı
```

---

## 📱 Bot Kullanımı

### Komutlar

- `/start` - Başlat
- `/analiz BTC` - Tam detaylı 7 katman analiz
- `/hizli BTC` - Hızlı özet
- `BTC` - Direkt sembol yaz (en hızlı)

### Desteklenen Varlıklar

**Kripto:** BTC, ETH, SOL, AVAX, XRP, DOGE, ADA, DOT, MATIC, BNB, LINK

**Hisseler:** AAPL, TSLA, MSFT, GOOGL, THYAO, GARAN, ISCTR...

**Emtialar:** ALTIN, PETROL, GUMUS

**Forex:** EURUSD, GBPJPY... (sembol olarak)

---

## 📊 Analiz Katmanları

1. **Fiyat Hareketi:** 38 mum formasyonu (Hammer, Engulfing, Doji...)
2. **Teknik Göstergeler:** RSI, MACD, Bollinger, SMA/EMA, ADX...
3. **Matematik:** Fibonacci, destek/direnç
4. **Piyasa Yapısı:** Trend analizi, likidite
5. **Temel Analiz:** On-chain metrikler (kripto) veya değerleme (hisse)
6. **Sentiment:** Fear & Greed Index
7. **Risk Yönetimi:** Stop-loss, pozisyon boyutu, R:R

---

## ⚙️ Railway Settings

### Otomatik Ayarlar (Elle Ayar Gerekmez)

Railway Dockerfile'ı otomatik algılayacak:

- ✅ Builder: DOCKERFILE (otomatik)
- ✅ Start Command: `python -u app.py` (Dockerfile'da)
- ✅ Health Check: `/health` endpoint
- ✅ PORT: Otomatik atanır

### Manuel Kontrol (Opsiyonel)

**Settings** → **Deploy:**
- Restart Policy: `ON_FAILURE` ✅
- Health Check Path: `/health`
- Health Check Timeout: 300s

---

## 🔧 Sorun Giderme

### Build Hatası

```bash
# requirements.txt var mı kontrol et
ls -la

# İçeriğini kontrol et
cat requirements.txt
```

### Bot Başlamıyor

Railway → Deployments → **View Logs**

**Görmek istediğin:**
```
✅ Flask server başlatıldı
✅ Bot polling modu başladı
```

**Hata varsa:**
```
❌ TELEGRAM_TOKEN yok → Variables ekle
❌ ModuleNotFoundError → requirements.txt kontrol et
```

### Environment Variables Eksik

Railway → Variables → Add Variable:
```
TELEGRAM_TOKEN = bot_token_buraya
GEMINI_API_KEY = gemini_key_buraya
```

---

## 💎 Örnek Çıktı

```
🎯 YÖNETİCİ ÖZETİ
KARAR: 🟢 GÜÇLÜ AL
Güven Skoru: %87
Risk: ORTA
Tez: Bullish Engulfing + RSI oversold...

📊 7 KATMAN ANALİZ
[Detaylı analiz...]

💼 İŞLEM PLANI
Giriş: $67,450
Stop-Loss: $64,200 (Risk: -4.8%)
Hedef 1: $72,800 (R:R = 1.6:1)

$10K hesap için: $4,167 pozisyon (risk $200)
```

---

## 📈 Teknik Stack

- **Backend:** Python 3.11
- **Bot Framework:** python-telegram-bot 20.8
- **AI:** Gemini 1.5 Flash
- **Data:** yfinance + pandas_ta
- **Server:** Flask
- **Deploy:** Railway (Docker)

---

## ⚠️ Disclaimer

Bu bot yatırım tavsiyesi vermez. Tüm finansal kararlar kullanıcının sorumluluğundadır.

---

## 📞 Destek

Sorun mu var? Railway Logs'u kontrol et:
Railway Dashboard → Deployments → View Logs

---

🦁 **PROMETHEUS AI v10.0** - Powered by Railway & Gemini AI