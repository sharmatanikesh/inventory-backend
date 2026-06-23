from abc import ABC, abstractmethod
from uuid import UUID
from typing import List, Optional, Dict
from sqlalchemy.orm import Session
from app.models.order import Order

class OrderRepositoryInterface(ABC):
    @abstractmethod
    def get_by_id(self, order_id: UUID) -> Optional[Order]:
        """Retrieve an order by ID."""
        pass

    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Order]:
        """Retrieve all orders with pagination."""
        pass

    @abstractmethod
    def create(self, customer_id: UUID, items: List[Dict]) -> Order:
        """Create and persist a new order with items, computing the total amount."""
        pass

    @abstractmethod
    def update_status(self, order_id: UUID, status: str) -> Optional[Order]:
        """Update an order's status."""
        pass

    @abstractmethod
    def count_total(self) -> int:
        """Count total orders."""
        pass


from sqlalchemy.orm import joinedload
from sqlalchemy import func
from app.models.order_item import OrderItem

class SQLAlchemyOrderRepository(OrderRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, order_id: UUID) -> Optional[Order]:
        return self.db.query(Order).options(joinedload(Order.items)).filter(Order.id == order_id).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Order]:
        return self.db.query(Order).options(joinedload(Order.items)).offset(skip).limit(limit).all()

    def create(self, customer_id: UUID, items: List[Dict]) -> Order:
        order = Order(customer_id=customer_id, status="pending")
        total_amount = 0.0
        for item in items:
            order_item = OrderItem(
                product_id=item["product_id"],
                quantity=item["quantity"],
                unit_price=item["unit_price"]
            )
            order.items.append(order_item)
            total_amount += float(item["quantity"]) * float(item["unit_price"])
        
        order.total_amount = total_amount
        self.db.add(order)
        self.db.commit()
        self.db.refresh(order)
        return order

    def update_status(self, order_id: UUID, status: str) -> Optional[Order]:
        order = self.get_by_id(order_id)
        if order:
            order.status = status
            if status == "cancelled":
                order.cancelled_at = func.now()
            self.db.commit()
            self.db.refresh(order)
        return order

    def count_total(self) -> int:
        return self.db.query(Order).count()
