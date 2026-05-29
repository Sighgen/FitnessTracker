FROM python:3.12-slim

WORKDIR /app

# curl til healthcheck + non-root user
RUN apt-get update && apt-get install -y curl \
    && rm -rf /var/lib/apt/lists/* \
    && useradd -m appuser

# Installer dependencies først (caching)
COPY backend/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Kopier kode
COPY backend/ ./backend/

# Data-mappen skal eksistere inden opstart
RUN mkdir -p backend/data \
    && chown -R appuser:appuser /app

EXPOSE 8000

# Healthcheck (kræver at du har /health endpoint i FastAPI)
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

USER appuser

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]