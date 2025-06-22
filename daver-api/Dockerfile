# daver-api/Dockerfile
FROM python:3.11-slim AS base
WORKDIR /app

# Install system dependencies
COPY daver-api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY daver-api/ .
COPY nlparser/             ./nlparser
COPY querygenerator/       ./querygenerator
COPY queryjudge/           ./queryjudge
COPY schemaanalyzer/       ./schemaanalyzer

EXPOSE 8000
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]