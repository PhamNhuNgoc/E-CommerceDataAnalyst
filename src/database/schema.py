import os
import sys

# Path Append
sys.path.append(os.path.abspath(os.curdir))

from src.database.connector import Base
from sqlalchemy import Column, Integer, BigInteger, String, Boolean

class Product(Base):
    __tablename__ = 'products'

    item_id = Column(BigInteger, primary_key=True)
    name = Column(String(255), nullable=False)
    url = Column(String(255), nullable=False)
    price = Column(String(255))
    rating = Column(String(255))
    num_review = Column(Integer, default=0)
    in_stock = Column(Boolean,  nullable=False)
    brand = Column(String(255))
    seller = Column(String(255))
    seller_id = Column(BigInteger,  nullable=False)
    original_price = Column(String(255))
