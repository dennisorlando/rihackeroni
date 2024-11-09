FROM python:3.13-slim

WORKDIR /app

RUN pip install --upgrade pip && pip install gunicorn
RUN apt update && apt install -y tini

COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY . /app

ENTRYPOINT ["/usr/bin/tini", "--", "flask", "run", "--host", "0.0.0.0", "--port", "8000"]

