# Тестовое задание:
Технологии: FastApi, docker-compose, PostgreSQL, SQLAlchemy, Телеграм бот

Реализовать микросервисное веб приложение для мониторинга цен на любом сайте, например, мвидео.

Необходимо предусмотреть следующий функционал:

1. Модуль HTTP API  С использованием библиотеки FastApi
Он должен содержать следующие маршруты:
1) Добавление нового товара на мониторинг (ссылка на товар)
2) Удаление товара
3) Получение списка товаров на мониторинге
4) Получение истории цен на товар.
2. Телеграм бот с аналогичным функционалом
3. Модуль мониторинга, который будет периодически получать новую цену товара:
При добавлении товара, необходимо получать только его название, описание и рейтинг (если есть).
Получать информацию можно просто через requests.
Записывать цену на товар необходимо раз в час.
4. БД для хранения информации (PostgreSQL)
Запуск кода через docker-compose, каждый модуль в отдельном контейнере. Как минимум модуль БД должен иметь volume для сохранения информации в нем.
Для работы с базой использовать либу SQLAlchemy.

Если будет время и желание, то кроме маршрутов бекенда, можно ещё сделать странички для этих маршрутов с помощью шаблонов Jinja2
 и обмазать bootstrapовскими классами для красоты, но это вообще не обязательно.

## Как развернуть проект:
### 1 Клонируем проект

```bash
git clone https://github.com/Yomorad/fastapi-monitoring.git
```

### 2 Прописываем свои конфиги в .env
```bash
TELEGRAM_BOT_TOKEN='your_bot_token' # Поставь новый токен от BotFather из телеги
```

### 3 Поднимаем контейнеры
```bash
docker compose up --build
# Completed!
# в конце работы выключаем контейнеры и удаляем привязанные тома
docker compose down -v
```

## Тестируем проект:

### Postman:
#### 1 GET http://0.0.0.0:8000/products/
![Запрос в Postman](./readme_images/image.png)
#### 2 DELETE http://0.0.0.0:8000/products/<<id>>
![Запрос в Postman](./readme_images/image1.png)
#### 3 POST http://0.0.0.0:8000/products/ 
    body:{"link_product": "https://sunlight.net/catalog/ring_146397.html"}
![Запрос в Postman](./readme_images/image2.png)
#### 4 GET http://0.0.0.0:8000/products/<<id>>/price-history
![Запрос в Postman](./readme_images/image3.png)

### Телеграм-бот:
#### /start

![Запрос в Telegram](./readme_images/image4.png)
#### /add

![Запрос в Telegram](./readme_images/image6.png)
#### /list

![Запрос в Telegram](./readme_images/image5.png)
#### /delete

![Запрос в Telegram](./readme_images/image8.png)
#### /history

![Запрос в Telegram](./readme_images/image7.png)
