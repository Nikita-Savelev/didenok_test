# Password Manager

## Описание

Менеджер паролей с RESTful API для создания, поиска и получения паролей.

## Как запустить проект

1. Убедитесь, что у вас установлен Docker и Docker Compose.

2. Склонируйте репозиторий:

   ```bash
   git clone https://github.com/Nikita-Savelev/didenok_test
   cd didenok_test
   ```
   
3. Запустите проект:
   ```bash
   docker-compose up --build
   ```
   
4. API будет доступен по адресу http://localhost:8000. Swager: /docs

## API

- POST /password/{service_name} - Создает пароль/заменяет существующий.
- GET /password/{service_name} - Получает пароль по имени сервиса.
- GET /password/?service_name={part_of_service_name} - Ищет пароли по имени сервиса.