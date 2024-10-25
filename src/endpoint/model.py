from pydantic import BaseModel, Field

class ProductRequest(BaseModel):
    id: int = Field(gt=0) 
    name: str = Field(min_length=1) 
    link: str = Field()
    price: float = Field(gt=0)

    class Config:
        orm_mode = True