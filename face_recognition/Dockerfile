
# ===== Builder =====
FROM python:3.11-bullseye AS builder

RUN apt-get update && apt-get install -y \
  build-essential \
  cmake \
  libopenblas-dev \
  liblapack-dev \
  libjpeg-dev \
  libpng-dev \
  libtiff-dev \
  libavcodec-dev \
  libavformat-dev \
  libswscale-dev \
  libsm6 \
  libxext6 \
  libgl1\
  libffi-dev \
  libwebp-dev \
  && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip wheel --wheel-dir=/wheels -r requirements.txt

# ===== Container final =====
FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
  libglib2.0-0 \
  libopenblas-dev \
  liblapack-dev \
  libjpeg-dev \
  libpng-dev \
  libtiff-dev \
  libsm6 \
  libxext6 \
  libgl1 \
  libffi-dev \
  libwebp-dev \
  && rm -rf /var/lib/apt/lists/*

RUN ln -s /usr/lib/x86_64-linux-gnu/libwebp.so.7 /usr/lib/x86_64-linux-gnu/libwebp.so.6 || true

COPY --from=builder /wheels /wheels
RUN pip install --no-cache-dir /wheels/*

COPY ./images/ ./images
COPY ./app/ ./app

CMD ["uvicorn", "app.server:app", "--host", "0.0.0.0", "--port", "8000"]
