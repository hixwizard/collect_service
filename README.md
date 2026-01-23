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
DEBUG = False подключит PostgreSQL
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
26000 записей суммарно (могуть быть ошибки сети docker)
```bash
docker compose exec app python manage.py mock_data
```

-------------------------------------------

#### Локальные команды:
```bash
python manage.py makemigrations
```
```bash
python manage.py migrate
```
```bash
python manage.py runserver
```
```bash
python manage.py ceratesuperuser
```
Создаст 26000 записей суммарно
```bash
python manage.py mock_data
```
Доступны опции, ниже пример
```bash
python manage.py mock_data --users 100 --collects 500 --payments 2000
```


