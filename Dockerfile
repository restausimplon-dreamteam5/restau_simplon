FROM python:3.12-slim

# TODO: Benjamin est-ce necessaire
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 

# TODO: privilèges utilisateurs

WORKDIR /app

# TODO: Benjamin pourquoi ????
# COPY requirements.txt .
# RUN pip install -r requirements.txt
# COPY app/ .

COPY app/ requirements.txt .

# --upgrade ???
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

# TODO: app.main:app ou main:app (à tester)
CMD uvicorn app.main:app --host 0.0.0.0 --port 8000

# docker build -t restausimplon-app:0.0.1 .

















































# WORKDIR /app

# COPY app/ .
# COPY .env .
# COPY requirements.txt .

# RUN pip install -r requirements.txt 

# EXPOSE 8000

# CMD uvicorn main.py --host 0.0.0.0 --port 8000
