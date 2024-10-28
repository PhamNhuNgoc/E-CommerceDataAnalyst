import os
import sys

# Path Append
sys.path.append(os.path.abspath(os.curdir))

from src.database.connector import Base
from sqlalchemy import Column, Integer, BigInteger, String, Boolean

class Product(Base):
    __tablename__ = 'products'

    item_id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(255), index=True)
    url = Column(String(255), index=False)
    price = Column(String(255))
    rating = Column(String(255))
    num_review = Column(Integer)
    in_stock = Column(Boolean)
    brand = Column(String(255))
    seller = Column(String(255))
    seller_id = Column(BigInteger)
    original_price = Column(String(255))
