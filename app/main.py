from fastapi import FastAPI
from app.routers.router import main_router

app = FastAPI(title="Inventory & Order Management API")

app.include_router(main_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Inventory & Order Management API"}

