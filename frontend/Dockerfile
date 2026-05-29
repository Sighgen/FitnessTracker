FROM python:3.12-slim

WORKDIR /app

# Installer dependencies først (caching)
COPY frontend/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Kopier kode
COPY frontend/ ./frontend/

EXPOSE 8501

# Streamlit konfiguration via flags — ingen config-fil nødvendig
CMD ["streamlit", "run", "frontend/app.py", \
     "--server.port=8501", \
     "--server.address=0.0.0.0", \
     "--server.headless=true", \
     "--browser.gatherUsageStats=false"]