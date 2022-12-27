from typing import List
from pydantic import BaseModel

class ProductBase(BaseModel):
    title: str
    description: str
    price: int
    discountPercentage: float
    rating: float
    stock: int
    brand: str
    category: str
    thumbnail: str
    images: List[str]

class Product(ProductBase):
    id: int

class UpdateProduct(ProductBase):
    pass
