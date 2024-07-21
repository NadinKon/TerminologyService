import os
import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "terminology_service.settings")
django.setup()
from django.contrib.auth.models import User

# Параметры суперпользователя
username = os.getenv("DJANGO_SUPERUSER_USERNAME", "admin")
email = os.getenv("DJANGO_SUPERUSER_EMAIL", "admin@example.com")
password = os.getenv("DJANGO_SUPERUSER_PASSWORD", "admin")

# Проверяем, существует ли пользователь с таким именем
if username and email and password:
    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username=username, email=email, password=password)
else:
    raise ValueError("Не установлены все необходимые переменные окружения для создания суперпользователя.")
