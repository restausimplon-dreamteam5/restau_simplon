FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN useradd -m appuser
USER appuser

COPY --chown=appuser:appuser migrations/ migrations/

COPY --chown=appuser:appuser alembic.ini .
    
CMD alembic upgrade head
