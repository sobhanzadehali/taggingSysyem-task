FROM python:3.10-slim
WORKDIR /app

EXPOSE 8000

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY ./requirements.txt .

RUN python -m pip install -r requirements.txt

COPY . /app/
