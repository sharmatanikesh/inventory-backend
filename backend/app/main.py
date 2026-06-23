from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.router import main_router
from app.utils.exceptions import AppException, app_exception_handler
from app.middleware.pagination import PaginationMiddleware
from app.utils.logger import setup_logger
from app.middleware.logging import StructuredLoggingMiddleware

# Initialize structured logging configuration
setup_logger()

app = FastAPI(title="Inventory & Order Management API")

# Order of middleware: outer-most runs first
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(StructuredLoggingMiddleware)
app.add_middleware(PaginationMiddleware)

app.add_exception_handler(AppException, app_exception_handler)

app.include_router(main_router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Inventory & Order Management API"}

