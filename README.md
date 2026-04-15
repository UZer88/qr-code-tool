# QR Code Tool

[![CI](https://github.com/UZer88/qr-code-tool/actions/workflows/ci.yml/badge.svg)](https://github.com/UZer88/qr-code-tool/actions/workflows/ci.yml)
[![Docker](https://img.shields.io/badge/docker-ready-blue)](https://www.docker.com/)
[![Deployed on Render](https://img.shields.io/badge/deployed%20on-render-blue)](https://qr-code-tool.onrender.com)

Простое приложение для генерации и сканирования QR-кодов.

## Возможности

- ✅ Создание QR-кодов из текста или URL
- ✅ Настройка размера QR-кода
- ✅ Сохранение QR-кода в файл
- ✅ Сканирование QR-кодов из изображений
- ✅ Копирование результата в буфер обмена
- ✅ Современный тёмный интерфейс (десктоп)
- ✅ Веб-версия (доступна из браузера)
- ✅ CLI-утилита для скриптов
- ✅ Docker-контейнер для лёгкого развёртывания

## Быстрый старт

### Веб-версия (онлайн)

Откройте в браузере: [https://qr-code-tool.onrender.com](https://qr-code-tool.onrender.com)

### Локально через Docker

```bash
docker run -p 8000:8000 ghcr.io/uzer88/qr-code-tool:latest
```
Затем откройте http://localhost:8000


### Требования
- Python 3.10 или выше

### Установка зависимостей
```bash
pip install qrcode[pil] pyzbar pillow pyperclip
```
## Запуск

```bash
python qr_generator.py
```

## Локальная установка
```bash
# Клонируйте репозиторий
git clone https://github.com/UZer88/qr-code-tool.git
cd qr-code-tool

# Создайте виртуальное окружение
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# Установите зависимости
pip install -r requirements.txt

# Запустите десктоп-версию
python qr_generator.py

# Или веб-версию
python web_app.py

# Или CLI-версию
python cli.py generate "Hello World" -o qr.png
python cli.py scan qr.png
```

## Тестирование
```bash
pytest tests/ -v
```

## Docker

### Сборка образа
```bash
docker build -t qr-code-tool .
```

### Запуск веб-версии
```bash
docker run -p 8000:8000 qr-code-tool
```

### Запуск CLI через Docker
```bash
docker run --rm -v $(pwd):/app qr-code-tool python cli.py generate "test" -o /app/output.png
```
## Использование CLI
```bash
# Генерация QR-кода
python cli.py generate "https://github.com/UZer88" -s 300 -o my_qr.png

# Сканирование QR-кода
python cli.py scan my_qr.png
```

## Технологии
- Python 3.12+
- Tkinter (десктопный GUI)
- FastAPI (веб-версия)
- qrcode, pyzbar, pillow
- pytest (тесты)
- Docker

## Лицензия
MIT

## Автор
UZer88