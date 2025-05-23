# Проект Habit Tracker - Система отслеживания привычек

## Описание:

 Habit Tracker - это Django-приложение для создания и отслеживания полезных привычек. Система позволяет пользователям:

- Создавать привычки с указанием места, времени и периодичности выполнения

- Устанавливать вознаграждения или связывать привычки между собой

- Получать Telegram-напоминания о выполнении привычек

- Просматривать публичные привычки других пользователей

## Функционал:

### Модули Habit

модуль приложения относящийся к привычке. Содержит модель привычки(models), валидаторы, сериалвйзеры

#### Валидаторы
validate_related_habit - проверяет, что связанная привычка является приятной

validate_reward_or_related - проверяет, что указано только одно: вознаграждение ИЛИ связанная привычка

validate_pleasant_habit - проверяет, что у приятной привычки нет вознаграждения или связанной привычки

validate_periodicity - проверяет, что периодичность не больше 7 дней

#### Сериализаторы

HabitSerializer - полный сериализатор для привычек с валидацией

Поля: все поля модели

Read-only: user, created_at

PublicHabitSerializer - упрощенный сериализатор для публичных привычек

Поля: id, place, time, action, periodicity, duration, is_public

### Telegram-бот

#### Функционал

Привязка аккаунта через команду /start <user_id>

Отправка напоминаний о привычках в указанное время

#### Настройка бота

Создайте бота через @BotFather

Укажите полученный токен в переменной окружения TELEGRAM_BOT_TOKEN

Для привязки аккаунта пользователь должен отправить команду /start <user_id> в бота

### Модули users

модуль приложения написанного при помощи фреймворка Django и содержит модель для работы с пользователями

### Модули  habit_tracker

содержит файлы конфигурации приложения


### Админ-панель

В админ-панели доступны следующие действия с привычками:

- Просмотр списка привычек (с отображением пользователя и действия)

- Создание/редактирование/удаление привычек

- Фильтрация по пользователям


## Настройки и запуска проекта

### Начальная настройка
1. Клонируйте репозиторий:
   ```chatinput
   git clone https://github.com/ваш-username/habit_tracker.git
   cd habit_tracker
   ```
2. Создайте файл .env на основе .env.example
3. Отредактируйте .env файл, указав свои настройки

### Начальная настройка
1. Соберите и запустите контейнеры:
```chatinput
   docker-compose up -d --build
   ```
2. Применение миграций:
```chatinput
   docker-compose exec web python manage.py migrate
   ```
3. Создание суперпользователя:
```chatinput
   docker-compose exec web python manage.py createsuperuser
   ```
4. Приложение будет доступно по адресу: http://localhost

### Настройка CI/CD
#### Требования
1. Аккаунт на Docker Hub
2. Сервер с установленными Docker и Docker Compose
3. SSH доступ к серверу
#### Настройка GitHub Secrets
Добавьте в настройках репозитория (Settings → Secrets → Actions) следующие секреты:
- SSH_KEY - Приватный SSH-ключ для доступа к серверу
- SSH_USER - Пользователь SSH (обычно root или ubuntu)
- SERVER_IP - IP-адрес сервера
- DOCKER_HUB_USERNAME - Логин Docker Hub
- DOCKER_HUB_ACCESS_TOKEN - Токен доступа Docker Hub
- POSTGRES_DB - Имя базы данных
- POSTGRES_USER - Пользователь PostgreSQL
- POSTGRES_PASSWORD - Пароль PostgreSQL
- SECRET_KEY - Секретный ключ Django
#### Работа CI/CD
При пуше в ветку main автоматически выполняются:
1. Проверка кода с помощью Flake8 
2. Запуск тестов с использованием PostgreSQL и Redis 
3. Сборка Docker-образов и загрузка в Docker Hub 
4. Деплой на сервер
### Развертывание на сервере
#### Подготовка сервера
1. Установите Docker и Docker Compose:
```chatinput
sudo apt-get update
sudo apt-get install docker.io docker-compose
sudo systemctl enable docker
sudo systemctl start docker
   ```
2. Создайте директорию для проекта:
```chatinput
mkdir -p ~/habit_tracker
   ```

## Тестирование

Для запуска тестов выполните:
```chatinput
python manage.py test habits
```
## Автор:
Ткачев Леонид Андреевич [e-mail] (tkachev1993adg@yandex.ru)

## Версия
от 17.05.2025 г.