# Image multi-stage : legere et sans outils de build dans l'image finale.
FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

# Execution en utilisateur non-root (bonne pratique de securite).
RUN useradd --create-home --uid 10001 appuser
USER appuser

EXPOSE 8000

# Gunicorn en production (2 workers) plutot que le serveur de dev Flask.
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "2", "app:app"]
