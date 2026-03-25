from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.schemas.order import OrderOut, OrderCreate
from app.db.database import get_db
from app.models import User, Product, OrderItem, Order
from app.auth.dependencies import get_current_user

router = APIRouter()

@router.post("/", response_model=OrderOut, status_code=status.HTTP_201_CREATED)
def create_order(
    order_in: OrderCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
  total_price = 0
  order_items_to_create = []

  # 1. Kiểm tra từng sản phẩm trong đơn hàng
  for item in order_in.items:
    product = db.query(Product).filter(Product.id == item.product_id).first()
        
    if not product:
      raise HTTPException(status_code=404, detail=f"Sản phẩm ID {item.product_id} không tồn tại")
        
    if product.stock < item.quantity:
      raise HTTPException(
        status_code=400, 
        detail=f"Sản phẩm {product.name} chỉ còn {product.stock} món, không đủ cung cấp"
      )

    item_price = product.price * item.quantity
    total_price += item_price
        
    # Tạo object OrderItem
    new_order_item = OrderItem(
      product_id=product.id,
      quantity=item.quantity,
      price_at_purchase=product.price
    )
    order_items_to_create.append(new_order_item)
        
    # 2. TRỪ KHO (Cập nhật trực tiếp vào object product)
    product.stock -= item.quantity

  # 3. Tạo đơn hàng chính (Order)
  new_order = Order(
    user_id=current_user.id,
    total_price=total_price,
    shipping_address=order_in.shipping_address,
    status="pending"
  )
    
  db.add(new_order)
  db.flush() # Lấy ID của đơn hàng vừa tạo nhưng chưa commit hẳn

  # 4. Gán Order ID cho từng item và lưu
  for item in order_items_to_create:
    item.order_id = new_order.id
    db.add(item)

  # 5. Hoàn tất giao dịch
  db.commit()
  db.refresh(new_order)
    
  return new_order

@router.get("/me", response_model=List[OrderOut])
def get_my_orders(
  db: Session = Depends(get_db),
  current_user: User = Depends(get_current_user)
):
  return db.query(Order).filter(Order.user_id == current_user.id).all()