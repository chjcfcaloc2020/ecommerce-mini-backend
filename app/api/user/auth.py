from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.schemas.user import UserOut, UserCreate
from app.db.database import get_db
from app.models import User
from app.core.security.hashing import verify_password, hash_password
from app.core.security.jwt import create_access_token

router = APIRouter()

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
  user = db.query(User).filter(User.username == form_data.username).first()

  if not user or not verify_password(form_data.password, user.hashed_password):
    raise HTTPException(status_code=400, detail="Username hoặc mật khẩu không chính xác")

  access_token = create_access_token(data={"sub": user.username})  
  return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register", response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
  db_user = db.query(User).filter(User.username == user.username).first()
  check_email_exsist = db.query(User).filter(User.email == user.email).first()

  if db_user or check_email_exsist:
    raise HTTPException(status_code=400, detail="Email hoặc username đã được đăng ký")
    
  new_user = User(
    username=user.username, 
    email=user.email, 
    hashed_password=hash_password(user.password),
  )

  db.add(new_user)
  db.commit()
  db.refresh(new_user)
  return new_user