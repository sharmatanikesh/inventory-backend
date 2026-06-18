from abc import ABC, abstractmethod
from uuid import UUID
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.product import Product

class ProductRepositoryInterface(ABC):
    @abstractmethod
    def get_by_id(self, product_id: UUID) -> Optional[Product]:
        """Retrieve a product by its ID."""
        pass

    @abstractmethod
    def get_by_sku(self, sku: str) -> Optional[Product]:
        """Retrieve a product by its SKU."""
        pass

    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Product]:
        """Retrieve all active products with pagination."""
        pass

    @abstractmethod
    def create(self, name: str, sku: str, price: float, quantity: int) -> Product:
        """Create and persist a new product."""
        pass

    @abstractmethod
    def update_quantity(self, product_id: UUID, quantity: int) -> Optional[Product]:
        """Update product quantity/stock level."""
        pass

    @abstractmethod
    def update(self, product_id: UUID, name: str, sku: str, price: float, quantity: int) -> Optional[Product]:
        """Update product details."""
        pass

    @abstractmethod
    def delete(self, product_id: UUID) -> None:
        """Soft-delete a product."""
        pass

    @abstractmethod
    def count_active(self) -> int:
        """Count total active products."""
        pass

    @abstractmethod
    def get_low_stock(self, threshold: int) -> List[Product]:
        """Retrieve active products under a stock threshold."""
        pass


class SQLAlchemyProductRepository(ProductRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, product_id: UUID) -> Optional[Product]:
        # Implementation skeleton - actual db query code excluded
        pass

    def get_by_sku(self, sku: str) -> Optional[Product]:
        # Implementation skeleton - actual db query code excluded
        pass

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Product]:
        # Implementation skeleton - actual db query code excluded
        pass

    def create(self, name: str, sku: str, price: float, quantity: int) -> Product:
        # Implementation skeleton - actual db query code excluded
        pass

    def update_quantity(self, product_id: UUID, quantity: int) -> Optional[Product]:
        # Implementation skeleton - actual db query code excluded
        pass

    def update(self, product_id: UUID, name: str, sku: str, price: float, quantity: int) -> Optional[Product]:
        # Implementation skeleton - actual db query code excluded
        pass

    def delete(self, product_id: UUID) -> None:
        # Implementation skeleton - actual db query code excluded
        pass

    def count_active(self) -> int:
        # Implementation skeleton - actual db query code excluded
        pass

    def get_low_stock(self, threshold: int) -> List[Product]:
        # Implementation skeleton - actual db query code excluded
        pass
