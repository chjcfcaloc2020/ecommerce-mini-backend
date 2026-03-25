from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserOut, UserCreate
from app.db.database import get_db
from app.models import User

router = APIRouter()

@router.post("/users", response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
  db_user = db.query(User).filter(User.email == user.email).first()
  if db_user:
    raise HTTPException(status_code=400, detail="Email đã được đăng ký")
    
  new_user = User(
    username=user.username, 
    email=user.email, 
    hashed_password=user.password
  )
  db.add(new_user)
  db.commit()
  db.refresh(new_user)
  return new_user