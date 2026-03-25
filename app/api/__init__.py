from fastapi import APIRouter
from app.api import user
from app.api import product

router = APIRouter()

router.include_router(user.router, prefix="/api")
router.include_router(product.router, prefix="/api")