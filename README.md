# Как запускать?

Все примеры можно запустить с помощью соответствующего bash-скрипта. Например, так:
`./run_auth.sh`

Чтобы добавить права на выполнение (при ошибке)
нужно выполнить `chmod +x run_auth.sh` для нужных файлов.

Либо можно запустить нужный сервер, а затем запустить к нему клиент. 
Например, выполнить `python3 auth/server.py` и в отдельном терминале `python auth/client.py`

# Список примеров

`./run_request_response.sh` - базовая обработка запросов и создание ответов

`./run_app_common_application.sh` - базовая структура приложения, добавление дополнительных полей к Application

`./run_app_custom_application.sh` - структура приложения с использование подмены тайпингов

`./run_routes.sh` - разные типы Route

`./run_middlewares.sh` - работа с middleware

`./run_validation.sh` - работа с валидацией и Swagger с помощью aiohttp-apispec

`./run_auth.sh` - работа с авторизацией с помощью aiohttp-session

