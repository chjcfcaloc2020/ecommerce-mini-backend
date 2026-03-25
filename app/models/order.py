from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base

class Order(Base):
  __tablename__ = "orders"
  id = Column(Integer, primary_key=True, index=True)
  user_id = Column(Integer, ForeignKey("users.id"))
  total_price = Column(Float)
  status = Column(String, default="pending")
  shipping_address = Column(String)
  created_at = Column(DateTime, default=func.now())

  owner = relationship("User", back_populates="orders")
  items = relationship("OrderItem", back_populates="order")