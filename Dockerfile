FROM python:3.12-slim

# Устанавливаем системные зависимости (нужны для pyzbar)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libzbar0 \
    libzbar-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Копируем только requirements (для кэширования слоёв)
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь код
COPY . .

# Открываем порт
EXPOSE 8000

# Отладочная команда — покажет точную ошибку в логах Render
CMD ["sh", "-c", "python -c \"from web_app import app; import uvicorn; uvicorn.run(app, host='0.0.0.0', port=8000)\""]