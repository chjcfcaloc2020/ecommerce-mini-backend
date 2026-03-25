from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class ProductBase(BaseModel):
  name: str
  description: str
  price: float
  stock: int
  category_id: int
  image_url: Optional[str] = None

class ProductCreate(ProductBase):
  pass

class ProductUpdate(BaseModel):
  name: Optional[str] = None
  description: Optional[str] = None
  price: Optional[float] = None
  stock: Optional[int] = None
  category_id: Optional[int] = None
  image_url: Optional[str] = None

class ProductOut(ProductBase):
  id: int
  created_at: datetime

  model_config = ConfigDict(from_attributes=True)