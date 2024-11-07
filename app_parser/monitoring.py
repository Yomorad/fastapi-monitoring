import requests
from parser import parse_product_data
from time import sleep
from config import FASTAPI_API_URL

def monitor_products():
    """
    Периодическая задача для обновления цен всех товаров.

    Получает список всех товаров из API и обновляет их цены, 
    извлекая данные с веб-страниц продуктов.

    В процессе работы делает паузу в 3 секунды между запросами 
    к API для добавления цен, чтобы избежать блокировки.
    """
    print("Running price update task...")
    response = requests.get(f"{FASTAPI_API_URL}/products/")
    products = response.json()
    for product in products:
        product_id = product["id"]
        product_link = product["link_product"]
        product_data = parse_product_data(product_link)
        json_data = {
            "price": product_data[0],
            "price_time": product_data[1]
        }
        response = requests.post(f"{FASTAPI_API_URL}/products/{product_id}/add-price", json=json_data)
        sleep(3)
