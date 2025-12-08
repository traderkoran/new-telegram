FROM python:3.11-slim

WORKDIR /app

# Minimum gerekli sistem paketleri
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    make \
    libopenblas-dev \
    liblapack-dev \
    libfreetype6-dev \
    libpng-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# pip güncelle
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Bağımlılıkları yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama dosyaları
COPY . .

# Railway Port
ENV PORT=8080
EXPOSE 8080

# Healthcheck — endpoint varsa çalışır
HEALTHCHECK CMD curl -f http://localhost:${PORT}/ || exit 1

CMD ["python", "-u", "app.py"]