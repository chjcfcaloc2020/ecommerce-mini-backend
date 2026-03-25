from fastapi import APIRouter
from app.api import user

router = APIRouter()

router.include_router(user.router, prefix="/api")
# router.include_router(users.router, prefix="/user", tags=["User"])