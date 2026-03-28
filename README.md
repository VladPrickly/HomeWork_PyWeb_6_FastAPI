# Задание

Нужно написать на fastapi и докеризировать сервис объявлений купли/продажи.

У объявлений должны быть следующие поля:
 - заголовок
 - описание
 - цена
 - автор
 - дата создания

Должны быть реализованы следующе методы:
 - Создание: `POST /advertisement`
 - Обновление: `PATCH /advertisement/{advertisement_id}`
 - Удаление: `DELETE /advertisement/{advertisement_id}`
 - Получение по id: `GET  /advertisement/{advertisement_id}`
 - Поиск по полям: `GET /advertisement?{query_string}`

## Предварительные требования
- Python 3.12+
- Git
- PostgreSQL
- Docker и Docker Compose
- Доступ к интернету

## Установка
1. Создайте виртуальное окружение:
python -m venv .venv

2. Активируйте виртуальное окружение:
- Windows:
  ```
  venv\Scripts\activate
  ```
- Linux/macOS:
  ```
  source venv/bin/activate
  ```
3. Установите зависимости:
pip install -r requirements.txt

4. Запуск приложения:
- создание БД: docker-compose up
- запуск приложения uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

Приложение запустится локально на http://localhost:8080/. БД будет создана при первом запуске.

## Эндпоинты

- Создание объявления
POST /advertisement
Content-Type: application/json
{
  "title": "Продам велосипед",
  "description": "Новый горный велосипед, 29 колёса",
  "price": 25000.00,
  "author": "Иван Петров"
}

- Получение объявления по ID
GET /advertisement/1
{
  "id": 1,
  "title": "Продам велосипед",
  "description": "Новый горный велосипед, 29 колёса",
  "price": 25000.00,
  "author": "Иван Петров",
  "created_at": "2024-03-28T10:30:00"
}

- Частичное обновление объявления (PATCH)
PATCH /advertisement/1
Content-Type: application/json
{
  "price": 23000.00
}

- Удаление объявления
DELETE /advertisement/1

- Поиск объявлений по параметрам
GET /advertisement/?title=велосипед&author=Иван&price=25000

5. API Документация
После запуска приложения автоматическая документация доступна по следующим адресам:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

6. Структура проекта

📦 HomeWork_PyWeb_6_FastAPI
├── 📁 app/
│   ├── 📄 main.py          # Точка входа, регистрация роутов
│   ├── 📄 models.py        # SQLAlchemy модели (таблицы БД)
│   ├── 📄 schemas.py       # Pydantic схемы (валидация данных)
│   ├── 📄 services.py      # Бизнес-логика (CRUD-операции)
│   ├── 📄 db.py            # Настройки подключения к БД
│   ├── 📄 lifespan.py      # Управление жизненным циклом приложения
│   └── 📄 dependencies.py  # Зависимости FastAPI (сессии БД)
├── 📄 docker-compose.yml   # Конфигурация Docker-сервисов
├── 📄 Dockerfile           # Инструкция сборки Docker-образа
├── 📄 requirements.txt     # Зависимости Python
├── 📄 .env.example         # Шаблон переменных окружения
├── 📄 .gitignore           # Исключения для Git
└── 📄 README.md            # Этот файл