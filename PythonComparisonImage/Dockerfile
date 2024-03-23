# Используем официальный базовый образ Python 3.10.12
FROM python:3.10.12-slim

# Установка необходимых системных зависимостей для PyQt5
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libfontconfig1 \
    libgl1 \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Установка рабочей директории в контейнере
WORKDIR /usr/src/app

# Копирование файла requirements.txt с зависимостями проекта в контейнер
COPY requirements.txt ./

# Установка Python зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Копирование содержимого локальной директории проекта в контейнер
COPY . .

# Команда для запуска приложения
CMD ["python", "./main.py"]
