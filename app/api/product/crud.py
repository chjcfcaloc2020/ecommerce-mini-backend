from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.models import Product
from app.models import User
from app.db.database import get_db
from app.schemas.product import ProductCreate, ProductOut, ProductUpdate
from app.auth.dependencies import check_admin

router = APIRouter()

@router.get("/", response_model=List[ProductOut])
def get_products(db: Session = Depends(get_db), skip: int = 0, limit: int = 10):
  return db.query(Product).offset(skip).limit(limit).all()

@router.get("/{id}", response_model=ProductOut)
def get_product(id: int, db: Session = Depends(get_db)):
  product = db.query(Product).filter(Product.id == id).first()
  if not product:
    raise HTTPException(status_code=404, detail="Sản phẩm không tồn tại")
  return product

@router.post("/", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
def create_product(
  product: ProductCreate, 
  db: Session = Depends(get_db),
  admin_user: User = Depends(check_admin)
):
  new_product = Product(**product.model_dump())
  db.add(new_product)
  db.commit()
  db.refresh(new_product)
  return new_product

@router.put("/{id}", response_model=ProductOut)
def update_product(
  id: int, 
  product_update: ProductUpdate, 
  db: Session = Depends(get_db),
  admin_user: User = Depends(check_admin)
):
  product_query = db.query(Product).filter(Product.id == id)
  product = product_query.first()

  if not product:
    raise HTTPException(status_code=404, detail="Sản phẩm không tồn tại")
    
  update_data = product_update.model_dump(exclude_unset=True) # chỉ cập nhật các field được gửi lên
  product_query.update(update_data)
  db.commit()
  return product

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
  id: int, 
  db: Session = Depends(get_db),
  admin_user: User = Depends(check_admin)
):
  product = db.query(Product).filter(Product.id == id).first()
  if not product:
    raise HTTPException(status_code=404, detail="Sản phẩm không tồn tại")
    
  db.delete(product)
  db.commit()
  return None