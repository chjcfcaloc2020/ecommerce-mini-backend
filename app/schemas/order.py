from pydantic import BaseModel, ConfigDict
from typing import List
from datetime import datetime
  
class OrderItemCreate(BaseModel):
  product_id: int
  quantity: int

class OrderCreate(BaseModel):
  shipping_address: str
  items: List[OrderItemCreate]

class OrderItemOut(BaseModel):
  product_id: int
  quantity: int
  price_at_purchase: float

  model_config = ConfigDict(from_attributes=True)

class OrderOut(BaseModel):
  id: int
  total_price: float
  status: str
  created_at: datetime
  items: List[OrderItemOut]

  model_config = ConfigDict(from_attributes=True)