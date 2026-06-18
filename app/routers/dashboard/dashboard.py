from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

class LowStockProduct(BaseModel):
    id: str
    name: str
    quantity: int

class DashboardSummaryResponse(BaseModel):
    total_products: int
    total_customers: int
    total_orders: int
    low_stock_products: List[LowStockProduct]

@router.get("/summary", response_model=DashboardSummaryResponse)
def get_dashboard_summary():
    # Skeleton implementation returning mock/dummy dashboard stats
    return {
        "total_products": 0,
        "total_customers": 0,
        "total_orders": 0,
        "low_stock_products": []
    }
