
# ===== Builder =====
FROM python:3.11-bookworm AS builder

ENV DEBIAN_FRONTEND=noninteractive \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

RUN set -eux; \
  apt-get update; \
  apt-get -y install --no-install-recommends \
    -o Acquire::Retries=5 \
    -o Acquire::http::Timeout="30" \
    -o Acquire::https::Timeout="30" \
    build-essential \
    cmake \
    pkg-config \
    libopenblas-dev \
    liblapack-dev \
    libjpeg-dev \
    libpng-dev \
    libtiff-dev \
    libwebp-dev \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libgl1 \
    libffi-dev; \
  rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Preferir binários reduz MUITO a chance de compilar dlib (se existir wheel pro seu target)
RUN python -m pip install --upgrade pip && \
    pip wheel --prefer-binary --wheel-dir=/wheels -r requirements.txt

# ===== Container final =====
FROM python:3.11-slim-bookworm

ENV DEBIAN_FRONTEND=noninteractive \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

RUN set -eux; \
  apt-get update; \
  apt-get -y install --no-install-recommends \
    -o Acquire::Retries=5 \
    -o Acquire::http::Timeout="30" \
    -o Acquire::https::Timeout="30" \
    libglib2.0-0 \
    libopenblas0-pthread \
    liblapack3 \
    libjpeg62-turbo \
    libpng16-16 \
    libtiff6 \
    libwebp7 \
    libsm6 \
    libxext6 \
    libgl1 \
    libffi8; \
  rm -rf /var/lib/apt/lists/*

COPY --from=builder /wheels /wheels
RUN pip install /wheels/*

COPY ./images/ ./images
COPY ./app/ ./app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
