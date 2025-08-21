FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 

WORKDIR /code

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN useradd -m appuser
USER appuser

COPY --chown=appuser:appuser pytest.ini .
COPY --chown=appuser:appuser tests/ tests/

EXPOSE 8000

CMD pytest tests/integrations/
