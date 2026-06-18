from abc import ABC, abstractmethod
from uuid import UUID
from typing import List, Optional
from app.models.product import Product

class ProductServiceInterface(ABC):
    @abstractmethod
    def get_product(self, product_id: UUID) -> Optional[Product]:
        """Fetch a single product."""
        pass

    @abstractmethod
    def get_all_products(self, skip: int = 0, limit: int = 100) -> List[Product]:
        """Fetch all products."""
        pass

    @abstractmethod
    def create_product(self, name: str, sku: str, price: float, quantity: int) -> Product:
        """Create a product after performing necessary validation checks."""
        pass

    @abstractmethod
    def update_stock(self, product_id: UUID, quantity: int) -> Optional[Product]:
        """Modify stock levels for a product."""
        pass
