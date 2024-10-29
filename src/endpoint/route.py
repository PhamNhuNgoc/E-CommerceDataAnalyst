from sqlalchemy.orm import Session
from starlette import status
from fastapi import FastAPI, Depends, HTTPException, Path

import os
import sys

# Path Append
sys.path.append(os.path.abspath(os.curdir))

from src.database.connector import get_db
import src.endpoint.crud as crud

router = FastAPI()

@router.get('/product/{product_id}', status_code=status.HTTP_200_OK)
def get_product_by_id(db: Session = Depends(get_db), product_id: int = Path(gt=0)):
    product = crud.get_item(db, product_id)
    if product is not None:
        return product
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product not found')

@router.get('/products', status_code=status.HTTP_200_OK)
def get_products(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    products = crud.get_items(db, skip, limit)
    if products:
        return products
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No products found')

@router.get('/products/category/{category}', status_code=status.HTTP_200_OK)
def get_products_by_category(category: str, db: Session = Depends(get_db)):
    products = crud.get_items_by_category(db, category)
    if products:
        return products
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No products found in category "{category}"')
