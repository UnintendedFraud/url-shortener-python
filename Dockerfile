from python:3.12-slim

workdir /app

# Install system dependencies and PostgreSQL development headers
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

copy ./requirement.txt /app/requirement.txt

run pip install --no-cache-dir --upgrade -r /app/requirement.txt

copy . /app

cmd ["fastapi", "run"]
