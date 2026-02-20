FROM python:3.12-slim

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    make \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем uv
RUN pip install uv

WORKDIR /app

# Копируем зависимости
COPY pyproject.toml uv.lock* ./

# Устанавливаем зависимости
RUN uv sync --frozen

# Копируем все файлы приложения
COPY . .

# Настраиваем переменные окружения
ENV FLASK_APP=src.main

# Запускаем приложение через make start-prod
CMD make start-prod