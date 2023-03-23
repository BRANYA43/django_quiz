FROM python:3.10.10-slim

RUN apt update && apt install -y mc vim python3-dev libpq-dev gcc curl

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRIREBYTECODE 1

RUN mkdir /opt/src
WORKDIR /opt/src

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    rm -f requirements.txt

COPY src .

EXPOSE 8890