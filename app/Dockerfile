# Usamos una imagen base ligera de Python compatible con Debian (lo que usa BB)
FROM python:3.9-slim-bullseye

# Variables de entorno para evitar archivos .pyc y buffers en logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# 1. Instalar dependencias del SISTEMA (Compiladores necesarios para GPIO)
# build-essential: necesario para compilar Adafruit_BBIO
# libgpiod2: librería moderna de linux para GPIO
RUN apt-get update && apt-get install -y \
    build-essential \
    libgpiod2 \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# 2. Copiar y gestión de requerimientos
COPY requirements.txt .
ENV CFLAGS="-fcommon"
RUN pip install --no-cache-dir -r requirements.txt

# 3. Copiar el código fuente
COPY . .

# 4. Comando de arranque - Shell interactivo
CMD ["/bin/bash"]
