### Приложение, сервис терминологии, который хранит коды данных и их контекст.

### Установка
Клонируйте репозиторий https://github.com/NadinKon/TerminologyService.git

### Использование
**Запустите проект с помощью Docker Compose:** <br>
docker-compose up --build

После успешного запуска контейнера, будут загружены тестовые данные, сами тесты будут запущены автоматически, создан суперпользователь и приложение будет доступно по адресу http://localhost:8000/

Админ панель доступна по адресу: http://localhost:8000/admin/ (логин/пароль: admin/admin)

Swagger документация доступна по адресу: http://localhost:8000/swagger/

ReDoc документация доступна по адресу: http://localhost:8000/redoc/

### API эндпоинты

- /api/refbooks/ - Получение списка справочников

- /api/refbooks/{id}/elements/ - Получение элементов заданного справочника <br>
пример запроса: /api/refbooks/1/elements/

- /api/refbooks/{id}/check_element/ - Валидация элемента справочника <br>
пример запроса: /api/refbooks/1/check_element/?code=1&value=Врач-терапевт&version=1.0
