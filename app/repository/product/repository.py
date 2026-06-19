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


from sqlalchemy import func

class SQLAlchemyProductRepository(ProductRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, product_id: UUID) -> Optional[Product]:
        return self.db.query(Product).filter(
            Product.id == product_id,
            Product.deleted_at.is_(None)
        ).first()

    def get_by_sku(self, sku: str) -> Optional[Product]:
        return self.db.query(Product).filter(
            Product.sku == sku,
            Product.deleted_at.is_(None)
        ).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Product]:
        return self.db.query(Product).filter(
            Product.deleted_at.is_(None)
        ).offset(skip).limit(limit).all()

    def create(self, name: str, sku: str, price: float, quantity: int) -> Product:
        product = Product(name=name, sku=sku, price=price, quantity=quantity)
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product

    def update_quantity(self, product_id: UUID, quantity: int) -> Optional[Product]:
        product = self.get_by_id(product_id)
        if product:
            product.quantity = quantity
            self.db.commit()
            self.db.refresh(product)
        return product

    def update(self, product_id: UUID, name: str, sku: str, price: float, quantity: int) -> Optional[Product]:
        product = self.get_by_id(product_id)
        if product:
            product.name = name
            product.sku = sku
            product.price = price
            product.quantity = quantity
            self.db.commit()
            self.db.refresh(product)
        return product

    def delete(self, product_id: UUID) -> None:
        product = self.get_by_id(product_id)
        if product:
            product.deleted_at = func.now()
            self.db.commit()

    def count_active(self) -> int:
        return self.db.query(Product).filter(
            Product.deleted_at.is_(None)
        ).count()

    def get_low_stock(self, threshold: int) -> List[Product]:
        return self.db.query(Product).filter(
            Product.deleted_at.is_(None),
            Product.quantity < threshold
        ).all()
