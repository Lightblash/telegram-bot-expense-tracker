# Telegram бот для учета личных расходов с записью в Google Sheets

Этот Telegram бот поможет вам вести учет личных расходов по категориям с возможностью записи данных в Google Sheets. Бот позволяет добавлять расходы через Telegram и просматривать их в Google Sheets.

## Требования

Для запуска бота вам нужно иметь:

- Python 3.8 или выше
- Токен Telegram бота
- Учетную запись Google и созданный проект в Google Cloud Console
- Файлы клиентского ключа и секретного ключа Google OAuth 2.0

## Установка и настройка

1. Клонируйте репозиторий:
```
git clone https://github.com/Lightblash/telegram-expense-bot.git
```

2. Перейдите в папку проекта:
```
cd telegram-expense-bot
```

3. Создайте файл .env и укажите в нем следующие переменные окружения:
```
TELEGRAM_API_TOKEN=<TELEGRAM_BOT_API_TOKEN>
TELEGRAM_ACCESS_IDS=<LIST_OF_USER_IDS>
GOOGLE_SPREADSHEET_TITLE=<GOOGLE_SPREADSHEET_TITLE>
GOOGLE_WORKSHEET_TITLE=<GOOGLE_WORKSHEET_TITLE>
GOOGLE_SERVICE_ACCOUNT=<GOOGLE_SERVICE_ACCOUNT>
```
4. Соберите Docker образ:
```
docker build -t telegram-expense-bot .
```

5. Запустите Docker контейнер:
```
docker run -d --name expense-bot --env-file .env telegram-expense-bot
```

## Использование

После запуска бота, отправьте ему команду /start, чтобы начать использование. Бот будет запрашивать у вас данные о расходах, такие как категория и сумма. После ввода данных бот добавит их в Google Sheets.

## Лицензия

Этот проект распространяется под лицензией MIT. Подробнее ознакомиться с лицензией можно в файле LICENSE.