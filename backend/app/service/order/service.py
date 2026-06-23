from uuid import UUID
from typing import List, Optional, Dict
from app.models.order import Order
from app.repository.order.repository import OrderRepositoryInterface
from app.repository.product.repository import ProductRepositoryInterface
from app.interfaces.order import OrderServiceInterface

from app.repository.customer.repository import CustomerRepositoryInterface
from app.utils.exceptions import (
    OrderNotFoundException,
    ProductNotFoundException,
    CustomerNotFoundException,
    InsufficientStockException
)

class OrderService(OrderServiceInterface):
    def __init__(
        self,
        order_repo: OrderRepositoryInterface,
        product_repo: ProductRepositoryInterface,
        customer_repo: CustomerRepositoryInterface
    ):
        self.order_repo = order_repo
        self.product_repo = product_repo
        self.customer_repo = customer_repo

    def get_order(self, order_id: UUID) -> Optional[Order]:
        return self.order_repo.get_by_id(order_id)

    def get_all_orders(self, skip: int = 0, limit: int = 100) -> List[Order]:
        return self.order_repo.get_all(skip=skip, limit=limit)

    def place_order(self, customer_id: UUID, items: List[Dict]) -> Order:
        customer = self.customer_repo.get_by_id(customer_id)
        if not customer:
            raise CustomerNotFoundException()
            
        validated_products = []
        for item in items:
            product = self.product_repo.get_by_id(item["product_id"])
            if not product:
                raise ProductNotFoundException()
            if product.quantity < item["quantity"]:
                raise InsufficientStockException(f"Insufficient stock for product {product.name}.")
            validated_products.append((item, product))
            
        # Deduct stock and build items list with price from database
        items_with_price = []
        for item, product in validated_products:
            new_qty = product.quantity - item["quantity"]
            self.product_repo.update_quantity(product.id, new_qty)
            items_with_price.append({
                "product_id": product.id,
                "quantity": item["quantity"],
                "unit_price": product.price
            })
            
        return self.order_repo.create(customer_id=customer_id, items=items_with_price)

    def cancel_order(self, order_id: UUID) -> Optional[Order]:
        order = self.order_repo.get_by_id(order_id)
        if not order:
            raise OrderNotFoundException()
            
        if order.status == "cancelled":
            return order
            
        # Restock items
        for item in order.items:
            product = self.product_repo.get_by_id(item.product_id)
            if product:
                new_qty = product.quantity + item.quantity
                self.product_repo.update_quantity(product.id, new_qty)
                
        return self.order_repo.update_status(order_id=order_id, status="cancelled")
