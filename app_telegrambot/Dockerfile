# Dockerfile for app_telegrambot
FROM python:3.12-slim

WORKDIR /app

# Устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install uvicorn

# Копируем исходный код
COPY . .

# Запуск приложения
CMD ["python", "main.py"]
