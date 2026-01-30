#### Сервис пожертвований для группового сбора средств.

-------------------------------------------

##### API
Ручки:
 - api/users/ - регистрация
 - api/collect/ - создание группового сбора, список сборов, детальный сбор
 - api/payment/ - создание пожертвования, список пожертвований, детальное пожертвование
 - docs/ - Swagger документация
 - admin/ - административная панель

-------------------------------------------

##### Отправка почты сервисом smtp.yandex
Для тестирования понадобится ключ smtp.yandex.ru, пример настроек в .env.example.
На почты автора сбора и пользователя, сделавшего пожертвование, приходят информационные письма.

-------------------------------------------

##### Кеширование всех запросов получения на 10 минут

-------------------------------------------

#### Инфраструктура:
Примечание: связка postgres+redis+localhost работает хорошо (через localhost).
Связка в docker работает медленно.
Сеть размечена на alpine образах, чувствительные данные нужно прятать в GitHub Actions.
Все примеры настроек в .env.example
DEBUG = True подключит SQLite
DEBUG = False подключит PostgreSQL+Redis
Запуск из infra/
```bash
docker compose up
```
Для создания суперпользователя
```bash
docker compose exec app python manage.py createsuperuser
```
Для генерации небольших тестовых данных
```bash
docker compose exec app python manage.py mock_data --users 10 --collects 50 --payments 200
```
26000 записей суммарно (могут быть ошибки сети docker)
```bash
docker compose exec app python manage.py mock_data
```

-------------------------------------------

#### Локальные команды:
```bash
poetry run python manage.py makemigrations api
```
```bash
poetry run python manage.py migrate
```
```bash
poetry run python manage.py runserver
```
```bash
poetry run python manage.py ceratesuperuser
```
Создаст 26000 записей суммарно
```bash
poetry run python manage.py mock_data
```
Доступны опции, ниже пример
```bash
poetry run python manage.py mock_data --users 100 --collects 500 --payments 2000
```

#### Основное

1. Базовая версия Python - 3.11.
2. В файле `requirements_style.txt` находятся зависимости для стилистики.
3. В каталоге `src` находится базовая структура проекта
4. В файле `srd/requirements.txt` прописываются базовые зависимости.
5. В каталоге `infra` находятся настроечные файлы проекта. Здесь же размещать файлы для docker compose.

##### Стилистика

Для стилизации кода используется пакеты `Ruff` и `Pre-commit`

Проверка стилистики кода осуществляется командой
```shell
poetry run ruff check
```

Если одновременно надо пофиксить то, что можно пофиксить автоматически, то добавляем параметр `--fix`
```shell
poetry run ruff check --fix
```

Что бы стилистика автоматически проверялась и поправлялась при комитах надо добавить hook pre-commit к git

```shell
pre-commit install
```
