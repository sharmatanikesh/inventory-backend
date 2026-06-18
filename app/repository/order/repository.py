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


class SQLAlchemyOrderRepository(OrderRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, order_id: UUID) -> Optional[Order]:
        # Implementation skeleton - actual db query code excluded
        pass

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Order]:
        # Implementation skeleton - actual db query code excluded
        pass

    def create(self, customer_id: UUID, items: List[Dict]) -> Order:
        # Implementation skeleton - actual db query code excluded
        pass

    def update_status(self, order_id: UUID, status: str) -> Optional[Order]:
        # Implementation skeleton - actual db query code excluded
        pass

    def count_total(self) -> int:
        # Implementation skeleton - actual db query code excluded
        pass
