from abc import ABC, abstractmethod
from uuid import UUID
from typing import List, Optional, Dict
from app.models.order import Order

class OrderServiceInterface(ABC):
    @abstractmethod
    def get_order(self, order_id: UUID) -> Optional[Order]:
        """Fetch details of a specific order."""
        pass

    @abstractmethod
    def get_all_orders(self, skip: int = 0, limit: int = 100) -> List[Order]:
        """Fetch all orders."""
        pass

    @abstractmethod
    def place_order(self, customer_id: UUID, items: List[Dict]) -> Order:
        """Place an order, verifying stock and computing totals."""
        pass

    @abstractmethod
    def cancel_order(self, order_id: UUID) -> Optional[Order]:
        """Cancel an order and restock items."""
        pass
