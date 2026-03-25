from fastapi import FastAPI
from app.db import database
from app.db.database import Base
from app.api import router

Base.metadata.create_all(bind=database.engine)

def create_app():
  app = FastAPI(title="Mini E-commerce API")
  # setup_cors
  app.include_router(router)
  return app

app = create_app()

@app.get("/")
async def root():
  return {"message": "Chào mừng đến với Ecommerce API!"}