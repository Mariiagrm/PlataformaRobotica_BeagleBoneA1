# Usamos Debian Bullseye (11) Slim, que es la base estable actual de BeagleBone
FROM python:3.9-slim-bullseye

# Metadatos
LABEL description="Entorno para BeagleBone con acceso a SysFS (GPIO/PWM)"

# Variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# CRÍTICO: Este flag permite compilar librerías antiguas (como Adafruit_BBIO) en GCC moderno
ENV CFLAGS="-fcommon"

# Directorio de trabajo
WORKDIR /app

# 1. Instalamos dependencias del sistema operativo
# 'build-essential' y 'gcc': para compilar
# 'libgpiod2': por si decides usar el estándar moderno
# 'nano': por si necesitas editar algo dentro del contenedor rápidamente
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    libgpiod2 \
    nano \
    && rm -rf /var/lib/apt/lists/*

# 2. Copiamos los requisitos (Asegúrate de que requirements.txt esté junto al Dockerfile)
COPY requirements.txt .

# 3. Instalamos dependencias de Python
# Usamos --no-cache-dir para mantener la imagen ligera
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 4. Copiamos el código fuente de tu proyecto
COPY . .

# 5. Comando por defecto (Mantiene el contenedor vivo si no hay script, o ejecuta tu main)
# Si prefieres que corra tu script directo cambia a: CMD ["python3", "src/main.py"]
CMD ["tail", "-f", "/dev/null"]