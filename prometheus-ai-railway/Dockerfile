# Base image
FROM python:3.11-slim

# Çalışma dizini
WORKDIR /app

# Sistem bağımlılıkları (Python bilimsel kütüphaneleri için)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    gfortran \
    make \
    libatlas-base-dev \
    liblapack-dev \
    libopenblas-dev \
    libfreetype6-dev \
    libpng-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Pip ve setuptools güncelle
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Python paketlerini yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama dosyalarını kopyala
COPY . .

# Railway port
ENV PORT=${PORT:-8080}
EXPOSE $PORT

# Opsiyonel: Sağlık kontrolü
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:${PORT}/health')" || exit 1

# Başlat
CMD ["python", "-u", "app.py"]

