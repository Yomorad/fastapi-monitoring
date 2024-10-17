from fastapi import APIRouter, HTTPException
from parser import parse_product_data

router = APIRouter()

@router.post("/parse-product")
def add_product(product_link: dict):
    try:
        product_data = parse_product_data(product_link["link"])
        return {
            "name": product_data[0],
            "description": product_data[1],
            "rate": product_data[2]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
