import os
import sys
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

# Path Append
sys.path.append(os.path.abspath(os.curdir))

from src.endpoint.model import ProductModel
from src.database.schema import Product

def get_item(db: Session, item_id: int):
    return db.query(Product).filter(Product.item_id == item_id).first()

def get_items(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Product).offset(skip).limit(limit).all()

def get_items_by_category(db: Session, category: str):
    return db.query(Product).filter(Product.brand == category).all()

def create_item(db: Session, item: ProductModel):
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

def upsert_item(db: Session, item: ProductModel):
    # Check if the item already exists
    existing_item = db.query(Product).filter(Product.item_id == item.item_id).first()
    
    if existing_item:
        # Update existing item
        for key, value in item.__dict__.items():
            if hasattr(existing_item, key) and key != "_sa_instance_state":
                setattr(existing_item, key, value)
        db.commit()
        db.refresh(existing_item)
        return existing_item
    else:
        # Insert new item
        new_item = Product(**item.__dict__)
        db.add(new_item)
        try:
            db.commit()
            db.refresh(new_item)
            return new_item
        except IntegrityError:
            db.rollback()
            raise ValueError("Failed to insert item. Possible integrity error.")