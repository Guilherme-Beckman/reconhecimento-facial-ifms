
# ===== Builder =====
FROM python:3.11-bullseye AS builder

# Instalar dependências do sistema para compilar dlib/face_recognition
RUN apt-get update && apt-get install -y \
  build-essential \
  cmake \
  libopenblas-dev \
  liblapack-dev \
  libx11-dev \
  libgtk-3-dev \
  libboost-all-dev \
  libjpeg-dev \
  libpng-dev \
  libtiff-dev \
  libavcodec-dev \
  libavformat-dev \
  libswscale-dev \
  libsm6 \
  libxext6 \
  libgl1-mesa-glx \
  libwebp-dev \
  libffi-dev \
  && rm -rf /var/lib/apt/lists/*

# Copiar e gerar wheels Python
COPY requirements.txt .
RUN pip wheel --wheel-dir=/wheels -r requirements.txt

# ===== Container final =====
FROM python:3.11-slim

# Instalar libs nativas necessárias no container final
RUN apt-get update && apt-get install -y \
  libopenblas-dev \
  liblapack-dev \
  libx11-6 \
  libsm6 \
  libxext6 \
  libgl1 \
  libjpeg-dev \
  libpng-dev \
  libwebp-dev \
  libffi-dev \
  && rm -rf /var/lib/apt/lists/*

# Copiar wheels compilados e instalar
COPY --from=builder /wheels /wheels
RUN pip install --no-cache-dir /wheels/*

# Copiar código
COPY ./images/ ./images
COPY ./app/ ./app

RUN ln -s /usr/lib/x86_64-linux-gnu/libwebp.so.7 /usr/lib/x86_64-linux-gnu/libwebp.so.6 || true
CMD ["python", "app/main.py"]
