from fastapi import APIRouter
from app.api.product import crud

router = APIRouter()

router.include_router(crud.router, prefix="/products", tags=["Product Management"])