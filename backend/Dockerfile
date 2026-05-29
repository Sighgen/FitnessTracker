FROM python:3.12-slim

WORKDIR /app

# Installer dependencies først (caching)
COPY backend/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Kopier kode
COPY backend/ ./backend/

# Data-mappen skal eksistere inden opstart
RUN mkdir -p backend/data

EXPOSE 8000

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]