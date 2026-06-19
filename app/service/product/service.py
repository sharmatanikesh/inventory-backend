from uuid import UUID
from typing import List, Optional
from app.models.product import Product
from app.repository.product.repository import ProductRepositoryInterface
from app.interfaces.product import ProductServiceInterface

from app.utils.exceptions import ProductNotFoundException, ConflictException, BadRequestException

class ProductService(ProductServiceInterface):
    def __init__(self, repository: ProductRepositoryInterface):
        self.repository = repository

    def get_product(self, product_id: UUID) -> Optional[Product]:
        return self.repository.get_by_id(product_id)

    def get_all_products(self, skip: int = 0, limit: int = 100) -> List[Product]:
        return self.repository.get_all(skip=skip, limit=limit)

    def create_product(self, name: str, sku: str, price: float, quantity: int) -> Product:
        if self.repository.get_by_sku(sku):
            raise ConflictException("Product SKU already exists.")
        if quantity < 0:
            raise BadRequestException("Product quantity cannot be negative.")
        return self.repository.create(name=name, sku=sku, price=price, quantity=quantity)

    def update_stock(self, product_id: UUID, quantity: int) -> Optional[Product]:
        if quantity < 0:
            raise BadRequestException("Product quantity cannot be negative.")
        product = self.repository.update_quantity(product_id=product_id, quantity=quantity)
        if not product:
            raise ProductNotFoundException()
        return product

    def update_product(self, product_id: UUID, name: str, sku: str, price: float, quantity: int) -> Product:
        product = self.repository.get_by_id(product_id)
        if not product:
            raise ProductNotFoundException()
        
        existing = self.repository.get_by_sku(sku)
        if existing and existing.id != product_id:
            raise ConflictException("Product SKU already exists.")
        if quantity < 0:
            raise BadRequestException("Product quantity cannot be negative.")
            
        return self.repository.update(
            product_id=product_id,
            name=name,
            sku=sku,
            price=price,
            quantity=quantity
        )

    def delete_product(self, product_id: UUID) -> None:
        if not self.repository.get_by_id(product_id):
            raise ProductNotFoundException()
        self.repository.delete(product_id)
