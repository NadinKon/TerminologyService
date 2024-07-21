# Используем образ Python
FROM python:3.11

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файл requirements в контейнер
COPY requirements.txt .

# Устанавливаем зависимости из requirements
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальные файлы проекта в контейнер
COPY . .

# Устанавливаем переменную окружения для настройки
ENV DJANGO_SETTINGS_MODULE=terminology_service.settings


# Запускаем сервер Django
CMD ["sh", "-c", "python manage.py migrate && \
                python manage.py loaddata refbooks/fixtures/initial_data.json && \
                python manage.py test && \
                python create_superuser.py && \
                python manage.py runserver 0.0.0.0:8000"]
