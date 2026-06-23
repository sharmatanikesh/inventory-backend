from uuid import UUID
from app.interfaces.order import OrderServiceInterface
from app.schemas.order import OrderCreateRequest
from app.utils.response import APIResponse
from app.utils.exceptions import OrderNotFoundException

class OrderController:
    def __init__(self, service: OrderServiceInterface):
        self.service = service

    def place_order(self, payload: OrderCreateRequest) -> APIResponse:
        dict_items = [{"product_id": item.product_id, "quantity": item.quantity} for item in payload.items]
        order = self.service.place_order(customer_id=payload.customer_id, items=dict_items)
        return APIResponse.ok(data=order, message="Order placed successfully")

    def get_order(self, order_id: UUID) -> APIResponse:
        order = self.service.get_order(order_id)
        if not order:
            raise OrderNotFoundException()
        return APIResponse.ok(data=order, message="Order retrieved successfully")

    def list_orders(self, skip: int = 0, limit: int = 100) -> APIResponse:
        orders = self.service.get_all_orders(skip=skip, limit=limit)
        return APIResponse.ok(data=orders, message="Orders retrieved successfully")

    def cancel_order(self, order_id: UUID) -> APIResponse:
        order = self.service.cancel_order(order_id)
        if not order:
            raise OrderNotFoundException()
        return APIResponse.ok(data=order, message="Order cancelled successfully")
