FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY core/ core/
COPY tools/ tools/
COPY static/ static/
COPY templates/ templates/
COPY uvicorn_log_config.ini .
COPY config.json .
COPY models.py .

EXPOSE 8002

HEALTHCHECK --interval=10m --timeout=10s \
  CMD curl -f http://localhost:8002/health || exit 1

CMD ["uvicorn", "core.server:app", "--host", "0.0.0.0", "--port", "8002", "--log-config", "uvicorn_log_config.ini"]
