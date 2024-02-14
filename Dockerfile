FROM python:3.12-slim

WORKDIR /app

RUN apt-get update
RUN apt-get install -y chromium chromium-driver

COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY src /app/src

ENV PYTHONPATH="/app"