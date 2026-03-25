from fastapi import APIRouter
from app.api.order import crud

router = APIRouter()

router.include_router(crud.router, prefix="/orders", tags=["Order Management"])