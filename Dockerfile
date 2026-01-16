# ==============================
# Base Image (Stable & Render-safe)
# ==============================
FROM python:3.11-slim

# ==============================
# Environment
# ==============================
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV ENV=docker

# ==============================
# Work Directory
# ==============================
WORKDIR /app

# ==============================
# System Dependencies
# ==============================
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# ==============================
# Python Dependencies
# ==============================
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# ==============================
# Copy Application Code
# ==============================
COPY . .

# ==============================
# Expose Port
# ==============================
EXPOSE 10000

# ==============================
# Start FastAPI
# ==============================
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "10000"]
