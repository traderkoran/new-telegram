FROM python:3.11-slim

WORKDIR /app

# Sistem bağımlılıkları
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Python paketleri
COPY requirements.txt
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# Uygulama dosyaları
COPY . .

# Port (Railway otomatik PORT verir)
EXPOSE ${PORT:-8080}

# Sağlık kontrolü (opsiyonel)
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:${PORT:-8080}/health')" || exit 1

# Başlat
CMD ["python", "-u", "app.py"]

