from pydantic import BaseModel
from typing import List

class LowStockProduct(BaseModel):
    id: str
    name: str
    quantity: int

class DashboardSummaryResponse(BaseModel):
    total_products: int
    total_customers: int
    total_orders: int
    low_stock_products: List[LowStockProduct]
