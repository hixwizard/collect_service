FROM python:3.11-alpine

WORKDIR /app

COPY requirements.txt .

RUN apk add --no-cache --virtual .build-deps \
    musl-dev libffi-dev openssl-dev \
    && pip install --no-cache-dir --compile -r requirements.txt \
    && apk del .build-deps

COPY . .

RUN mkdir -p /app/media /app/static