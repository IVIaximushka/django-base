# "ПРОчиталка"

Учебный проект для модуля "Принципы работы серверной части платформ управления данными"

## Запуск проекта для разработки
- `python -m venv venv` - создание виртуального окружения
- `source venv/scripts/activate` - войти в виртуальное окружение
- `pip install -r requirements.txt` - установка зависимостей
- установите [PostgreSQL](https://www.postgresql.org/)
- `docker-compose up -d` - запустить дополнительные сервисы в Docker.
- `python manage.py migrate` - применить миграции
- `python manage.py runserver` - запусить сервер для разработки на http://127.0.0.1:8000
