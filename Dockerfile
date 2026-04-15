FROM python:3.12-slim

# Устанавливаем системные зависимости (нужны для работы pyzbar)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libzbar0 \
    libzbar-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Копируем и устанавливаем ТОЛЬКО продакшен зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальной код
COPY . .

# Указываем порт
EXPOSE 8000

# Запускаем веб-сервер
CMD ["uvicorn", "web_app:app", "--host", "0.0.0.0", "--port", "8000"]