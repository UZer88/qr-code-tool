FROM python:3.12-slim

# Устанавливаем системные зависимости (нужны для pyzbar)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libzbar0 \
    libzbar-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Копируем зависимости и устанавливаем
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Переменная окружения для Python
ENV PYTHONPATH=/app

# Команда для запуска GUI (Tkinter не работает в Docker без дисплея!)
# Поэтому сделаем две версии: GUI и CLI

# Для CLI-версии (генерация и сканирование через командную строку)
# CMD ["python", "cli.py"]

# Для веб-версии (рекомендую, сделаем позже)
# CMD ["uvicorn", "web_app:app", "--host", "0.0.0.0", "--port", "8000"]