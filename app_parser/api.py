from fastapi import APIRouter, HTTPException
from parser import parse_product_data

router = APIRouter()

@router.post("/parse-product")
def add_product(product_link: dict):
    """
    Парсит информацию о продукте по предоставленной ссылке.

    Args:
        product_link (dict): Словарь, содержащий ссылку на продукт.
                             Ожидается ключ "link".

    Returns:
        dict: Словарь с данными о продукте, включая:
            - name (str): Название продукта.
            - description (str): Описание продукта.
            - rate (str|None): Рейтинг продукта (или None, если отсутствует).

    Raises:
        HTTPException: Если возникает ошибка при парсинге продукта.
    """
    try:
        product_data = parse_product_data(product_link["link"])
        return {
            "name": product_data[0],
            "description": product_data[1],
            "rate": product_data[2]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
