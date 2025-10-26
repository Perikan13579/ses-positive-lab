FROM python:3.12-slim-bookworm 

WORKDIR /app

RUN apt-get update && apt-get install -y \
  build-essential \
  && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
  && python -m spacy download ja_core_news_sm

COPY . .

EXPOSE 8000