# Используем официальный Python-образ
FROM python:3.11-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем зависимости и исходники
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

# Указываем порт
EXPOSE 8080

# Команда запуска
CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]
