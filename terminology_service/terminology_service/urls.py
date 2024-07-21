from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Создаем представление для Swagger и ReDoc
schema_view = get_schema_view(
    openapi.Info(
        title="Refbook API",  # Название API
        default_version='v1',  # Версия API
        description="API для управления справочниками",  # Описание
    ),
    public=True,  # Делаем схему общедоступной
)

urlpatterns = [
    path('admin/', admin.site.urls),  # Маршрут для админки
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),  # Маршрут для Swagger
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),  # Маршрут ReDoc
    path('api/', include('refbooks.urls')),  # Включение маршрутов приложения
]
