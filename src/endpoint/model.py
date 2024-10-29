from typing import Optional
from pydantic import BaseModel, Field

class ProductModel(BaseModel):
    item_id: int = Field(..., gt=0, alias='item_id')
    name: str = Field(..., min_length=1, alias='name') 
    url: str = Field(..., alias='url')
    price: Optional[float] = Field(..., gt=0, alias='price')
    rating: Optional[str] = Field(None, alias='rating')
    num_review: Optional[int] = Field(0, ge=0, alias='num_review')
    in_stock: Optional[bool] = Field(..., alias='in_stock')
    brand: Optional[str] = Field(None, alias='brand')
    seller: Optional[str] = Field(None, alias='seller')
    seller_id: int = Field(..., gt=0, alias='seller_id')
    original_price: Optional[float] = Field(None, alias='original_price')

    class Config:
        orm_mode = True
        