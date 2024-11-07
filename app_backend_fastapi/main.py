import os
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException
import requests
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models, schemas

load_dotenv()
# управляю миграциями через alembic, но на всякий случай оставлю заглушку если потребуется
# models.Base.metadata.create_all(bind=engine)

API_URL_PARSER = os.getenv("API_URL_PARSER")

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/products/", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    """
    Создает новый продукт на основе полученной ссылки.

    Args:
        product (schemas.ProductCreate): Данные о продукте, включая ссылку на него.
        db (Session, optional): Объект сессии базы данных. По умолчанию получает зависимость.

    Returns:
        schemas.Product: Объект созданного продукта с данными из базы данных, 
                         или с ограниченной информацией в случае ошибки парсинга.
    """
    link_product = product.link_product
    try: 
        response = requests.post(f"{API_URL_PARSER}/parse-product", json={"link": link_product})  # Изменили GET на POST
        if response.status_code == 200:
            data = response.json()
            name_product = data.get('name')
            description = data.get('description')
            rate = data.get('rate')
            
            db_product = models.Product(
                link_product=link_product,
                name_product=name_product, 
                description=description,
                rate=rate
            )
            db.add(db_product)
            db.commit()
            db.refresh(db_product)
            return db_product
        else:
            print(f"Error: {response.status_code}")
    except Exception as e:
        print(f"Произошла ошибка с парсингом: {e} // поэтому добавили только ссылку в БД")
        db_product = models.Product(
            link_product=link_product,
            name_product=None,  
            description=None,
            rate=None,
        )
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product


@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    """
    Удаляет продукт из базы данных по его идентификатору.

    Args:
        product_id (int): Идентификатор продукта, который нужно удалить.
        db (Session, optional): Объект сессии базы данных. По умолчанию получает зависимость.

    Raises:
        HTTPException: Если продукт не найден с данным идентификатором.
    
    Returns:
        dict: Подтверждение об удалении продукта.
    """
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(db_product)
    db.commit()
    return {"detail": "Product deleted"}


@app.get("/products/", response_model=list[schemas.Product])
def read_products(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Читает список продуктов из базы данных с возможностью пагинации.

    Args:
        skip (int, optional): Количество пропущенных продуктов для пагинации. По умолчанию 0.
        limit (int, optional): Максимальное количество продуктов для возврата. По умолчанию 10.
        db (Session, optional): Объект сессии базы данных. По умолчанию получает зависимость.

    Returns:
        list[schemas.Product]: Список объектов продуктов.
    """
    products = db.query(models.Product).offset(skip).limit(limit).all()
    return products


@app.get("/products/{product_id}/price-history", response_model=list[schemas.PriceHistoryBase])
def read_price_history(product_id: int, db: Session = Depends(get_db)):
    """
    Возвращает историю цен для указанного продукта.

    Args:
        product_id (int): Идентификатор продукта, история цен которого нужна.
        db (Session, optional): Объект сессии базы данных. По умолчанию получает зависимость.

    Raises:
        HTTPException: Если продукт не найден с данным идентификатором.

    Returns:
        list[schemas.PriceHistoryBase]: История цен для указанного продукта.
    """
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product.price_histories


@app.post("/products/{product_id}/add-price", response_model=schemas.PriceHistoryBase)
def add_price(product_id: int, price_data: schemas.PriceHistoryBase, db: Session = Depends(get_db)):
    """
    Добавляет новую цену для указанного продукта.

    Args:
        product_id (int): Идентификатор продукта, для которого добавляется новая цена.
        price_data (schemas.PriceHistoryBase): Данные о цене, включая цену и время.
        db (Session, optional): Объект сессии базы данных. По умолчанию получает зависимость.

    Raises:
        HTTPException: Если продукт не найден с данным идентификатором.

    Returns:
        schemas.PriceHistoryBase: Объект с добавленной ценой и данными о времени.
    """
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    price_history = models.PriceHistory(
        product_id=product_id,
        price=price_data.price,
        price_time=price_data.price_time
    )
    db.add(price_history)
    db.commit()
    db.refresh(price_history)
    return price_history
