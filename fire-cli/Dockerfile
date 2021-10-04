# syntax=docker/dockerfile:1

FROM python:3.7-slim-buster

COPY requirements.txt /tmp/requirements.txt

RUN python -m pip install -r /tmp/requirements.txt

COPY ./ /app

ENV PYTHONPATH=/app:${PYTHONPATH}

WORKDIR /app

CMD ["python", "main.py"]