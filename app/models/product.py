from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base

class Product(Base):
  __tablename__ = "products"
  id = Column(Integer, primary_key=True, index=True)
  name = Column(String, index=True)
  description = Column(Text)
  price = Column(Float)
  stock = Column(Integer)
  image_url = Column(String, nullable=True)
  category_id = Column(Integer, ForeignKey("categories.id"))
  created_at = Column(DateTime, default=func.now())

  category = relationship("Category", back_populates="products")