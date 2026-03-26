FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    nginx nodejs npm curl \
    && rm -rf /var/lib/apt/lists/*

RUN pip install uv

WORKDIR /app

COPY pyproject.toml uv.lock* ./
RUN uv sync --frozen

COPY package.json package-lock.json ./
RUN npm install

COPY . .
RUN npm run build
RUN mkdir -p /app/public && cp -r ./node_modules/@hexlet/project-devops-deploy-crud-frontend/dist/. /app/public/

COPY nginx.conf /etc/nginx/sites-available/default

# Запускаем nginx в фоне и flask на переднем плане
CMD service nginx start && uv run flask run --host=0.0.0.0 --port=$FLASK_PORT