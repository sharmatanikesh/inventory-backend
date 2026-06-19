from app.utils.response import APIResponse

class DashboardController:
    def get_summary(self) -> APIResponse:
        summary = {
            "total_products": 0,
            "total_customers": 0,
            "total_orders": 0,
            "low_stock_products": []
        }
        return APIResponse.ok(data=summary, message="Dashboard summary retrieved successfully")
