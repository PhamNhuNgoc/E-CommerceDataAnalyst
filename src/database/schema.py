from src.database.connector import Base
from sqlalchemy import Column, Integer, String, Float, Boolean

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, primary_key=False, index=True)
    link = Column(String, index=False)
    price = Column(Float)
