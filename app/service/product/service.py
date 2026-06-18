from uuid import UUID
from typing import List, Optional
from app.models.product import Product
from app.repository.product.repository import ProductRepositoryInterface
from app.interfaces.product import ProductServiceInterface

class ProductService(ProductServiceInterface):
    # Constructor Injection: we depend on the interface, not SQLAlchemy concrete class
    def __init__(self, repository: ProductRepositoryInterface):
        self.repository = repository

    def get_product(self, product_id: UUID) -> Optional[Product]:
        # Implementation skeleton - business logic excluded
        pass

    def get_all_products(self, skip: int = 0, limit: int = 100) -> List[Product]:
        # Implementation skeleton - business logic excluded
        pass

    def create_product(self, name: str, sku: str, price: float, quantity: int) -> Product:
        # Implementation skeleton - business logic excluded
        pass

    def update_stock(self, product_id: UUID, quantity: int) -> Optional[Product]:
        # Implementation skeleton - business logic excluded
        pass
