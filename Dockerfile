FROM python:3.12.6-slim

RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /organizations

COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock

RUN pip install --upgrade pip \
    && pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-root --only main

COPY . .

RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /organizations
USER appuser

EXPOSE 8000