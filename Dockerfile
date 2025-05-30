FROM python:3.12.6-slim

RUN apt-get update && apt-get install -y libpq-dev

WORKDIR /organizations

COPY /pyproject.toml /pyproject.toml

RUN pip install --upgrade pip \
  && pip install poetry \
  && poetry config virtualenvs.create false \
  && poetry install

COPY . .
