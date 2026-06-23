from app.utils.response import APIResponse
from app.repository.product.repository import ProductRepositoryInterface
from app.repository.customer.repository import CustomerRepositoryInterface
from app.repository.order.repository import OrderRepositoryInterface

class DashboardController:
    def __init__(
        self,
        product_repo: ProductRepositoryInterface,
        customer_repo: CustomerRepositoryInterface,
        order_repo: OrderRepositoryInterface
    ):
        self.product_repo = product_repo
        self.customer_repo = customer_repo
        self.order_repo = order_repo

    def get_summary(self) -> APIResponse:
        total_products = self.product_repo.count_active()
        total_customers = self.customer_repo.count_active()
        total_orders = self.order_repo.count_total()
        low_stock = self.product_repo.get_low_stock(threshold=10)
        
        low_stock_list = [
            {
                "id": str(p.id),
                "name": p.name,
                "quantity": p.quantity
            } for p in low_stock
        ]
        
        summary = {
            "total_products": total_products,
            "total_customers": total_customers,
            "total_orders": total_orders,
            "low_stock_products": low_stock_list
        }
        return APIResponse.ok(data=summary, message="Dashboard summary retrieved successfully")
