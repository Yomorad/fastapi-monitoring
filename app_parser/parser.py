from datetime import datetime
import requests
from bs4 import BeautifulSoup

# Функция для парсинга информации о продукте
def parse_product_data(link):
    html = requests.get(link).text
    soup = BeautifulSoup(html, 'lxml')
    
    # Парсинг данных продукта
    name_product = soup.find('h1', class_='supreme-product-card__info-name-title').text
    description_section = soup.find('ul', class_='supreme-product-card-collapsible-block__inner')
    description_items = description_section.find_all('li')
    description = '\n'.join(item.text for item in description_items)

    # Обработка возможного отсутствия рейтинга
    try:
        rate = soup.find('span', class_='supreme-product-card__info-name-reviews-rate').text
    except AttributeError:
        rate = None

    return name_product, description, rate

# Функция для обновления цены продукта
def update_price(link):
    html = requests.get(link).text
    soup = BeautifulSoup(html, 'lxml')
    new_price = soup.find('span', class_='supreme-product-card__price-discount-price').text
    new_price = ''.join(filter(str.isdigit, new_price))
    timestamp = datetime.now()
    return new_price, timestamp
