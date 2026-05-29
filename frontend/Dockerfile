FROM python:3.12-slim

WORKDIR /app

# Installér curl (til healthcheck) + lav non-root user
RUN apt-get update && apt-get install -y curl \
    && rm -rf /var/lib/apt/lists/* \
    && useradd -m appuser

# Installer dependencies først (caching)
COPY frontend/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Kopier kode
COPY frontend/ ./frontend/

# Ejerskab (god praksis)
RUN chown -R appuser:appuser /app

EXPOSE 8501

# Healthcheck (Streamlit internal endpoint)
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
  CMD curl -f http://localhost:8501/_stcore/health || exit 1

USER appuser

CMD ["streamlit", "run", "frontend/app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true", "--browser.gatherUsageStats=false"]