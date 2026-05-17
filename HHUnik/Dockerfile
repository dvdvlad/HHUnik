FROM python:3.12-slim

# Принудительно заставляем apt использовать IPv4 и проксируем его, если передан аргумент
RUN echo 'Acquire::ForceIPv4 "true";' > /etc/apt/apt.conf.d/99force-ipv4

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    build-essential \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Скачиваем и запускаем установщик Yandex Cloud CLI
RUN curl -sSL https://storage.yandexcloud.net/yandexcloud-yc/install.sh | bash

# Создаем символическую ссылку для глобального доступа к yc
RUN ln -s /root/yandex-cloud/bin/yc /usr/local/bin/yc

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . /app/

RUN chmod +x ./entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]