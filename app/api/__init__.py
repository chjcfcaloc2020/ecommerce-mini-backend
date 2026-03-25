from fastapi import APIRouter
from app.api.user import auth

router = APIRouter()

router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
# router.include_router(users.router, prefix="/user", tags=["User"])