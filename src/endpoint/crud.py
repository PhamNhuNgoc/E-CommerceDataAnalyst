from typing import Annotated, List
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette import status
from pydantic import BaseModel, Field
from fastapi import FastAPI, Depends, HTTPException, Path

import os
import sys

# Path Append
sys.path.append(os.path.abspath(os.curdir))

from src.database.schema import Product
from src.database.connector import Base, create_engine_instance, get_db
from src.endpoint.model import ProductRequest

router = FastAPI()

Base.metadata.create_all(bind=create_engine_instance)
db_dependency = Annotated[Session, Depends(get_db)]

@router.get('/product/{product_id}', status_code=status.HTTP_200_OK)
async def get_product_by_id(db: db_dependency, product_id: int = Path(gt=0)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is not None:
        return product
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product not found')

@router.post('/product', status_code=status.HTTP_201_CREATED)
async def create_product(db: db_dependency, product_request: ProductRequest):
    new_product = Product(**product_request.model_dump())

    db.add(new_product)
    db.commit()

@router.put('/product/{product_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_product(db: db_dependency, product_request: ProductRequest, product_id: int = Path(gt=0)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product not found')
    
    # Update product fields from request
    for var, value in vars(product_request).items():
        setattr(product, var, value) if value else None

    db.commit()

@router.delete('/product/{product_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(db: db_dependency, product_id: int = Path(gt=0)):
    product = db.query(Product).filter(Product.id == product_id).first()

    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product not found')
    
    db.delete(product)
    db.commit()