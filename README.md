Task Manager (Pet Project)



Pet-проект на FastAPI, демонстрирующий backend-навыки.

Проект представляет собой простой менеджер задач с авторизацией пользователей

и фоновой обработкой.



==================================================



ВОЗМОЖНОСТИ



\- REST API

\- JWT-аутентификация

\- CRUD для задач

\- Фоновые задачи через Celery

\- Redis (broker + cache)

\- Docker / Docker Compose

\- CI/CD (GitHub Actions)



==================================================



СТЕК ТЕХНОЛОГИЙ



\- Python 3.12

\- FastAPI

\- SQLAlchemy

\- PostgreSQL

\- Redis

\- Celery

\- JWT (Auth)

\- Docker / Docker Compose

\- uv (менеджер зависимостей)

\- GitHub Actions (CI/CD)



==================================================



ФУНКЦИОНАЛЬНОСТЬ



\- Регистрация и логин пользователей

\- JWT-аутентификация

\- CRUD операции для задач

\- Задачи принадлежат конкретному пользователю

\- Фоновые задачи через Celery

\- Redis используется как брокер и кеш

\- Healthcheck endpoint

\- CI:

&nbsp; - проверка Python-кода

&nbsp; - сборка Docker-образа

\- CD:

&nbsp; - сборка и публикация Docker-образа в GHCR



==================================================



ЗАПУСК ПРОЕКТА ЛОКАЛЬНО (БЕЗ DOCKER)



1\. Клонировать репозиторий



git clone https://github.com/kukushkinace1/task-manager-pet.git

cd task-manager-pet



2\. Установить зависимости



uv sync



3\. Создать .env

Создать файл .env на основе .env.example и заполнить значения.



4\. Запустить приложение



uv run uvicorn main:app --reload



Swagger будет доступен по адресу:

http://localhost:8000/docs



==================================================



ЗАПУСК ЧЕРЕЗ DOCKER COMPOSE



1\. Создать .env



cp .env.example .env



2\. Запуск



docker compose up --build



Будут запущены:

\- API (FastAPI)

\- PostgreSQL

\- Redis

\- Celery worker



API доступно по адресу:

http://localhost:8000



==================================================



АУТЕНТИФИКАЦИЯ



Используется JWT Bearer Token.



Регистрация:

POST /auth/register



Логин:

POST /auth/login



В ответе возвращается access\_token.

Его нужно передавать в заголовке:



Authorization: Bearer <token>



==================================================



HEALTHCHECK



GET /health



Ответ:

{ "status": "ok" }



==================================================



CI / CD



CI:

\- запускается при push в main

\- запускается при pull request

\- проверяет корректность Python-кода

\- проверяет сборку Docker-образа



CD:

\- при push в main

\- собирается Docker-образ

\- публикуется в GitHub Container Registry (GHCR)



==================================================



СТРУКТУРА ПРОЕКТА



|

|--- core/           (конфигурация, безопасность, Celery)

|--- models/         (SQLAlchemy модели)

|--- schemas/        (Pydantic схемы)

|--- routers/        (API роуты)

|--- main.py         (точка входа FastAPI)

|--- docker-compose.yml

|--- Dockerfile

|--- pyproject.toml

|--- .github/

&nbsp;   |-- workflows/  (CI/CD)



==================================================



ВОЗМОЖНЫЕ УЛУЧШЕНИЯ



\- Alembic миграции

\- Тесты (pytest)

\- Redis cache для GET /tasks

\- Logout через blacklist токенов

\- Rate limiting

\- Production-конфигурация

