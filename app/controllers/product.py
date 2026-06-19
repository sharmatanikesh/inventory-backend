from uuid import UUID
from app.interfaces.product import ProductServiceInterface
from app.schemas.product import ProductCreateRequest
from app.utils.response import APIResponse
from app.utils.exceptions import ProductNotFoundException

class ProductController:
    def __init__(self, service: ProductServiceInterface):
        self.service = service

    def create_product(self, payload: ProductCreateRequest) -> APIResponse:
        product = self.service.create_product(
            name=payload.name,
            sku=payload.sku,
            price=payload.price,
            quantity=payload.quantity
        )
        return APIResponse.ok(data=product, message="Product created successfully")

    def get_product(self, product_id: UUID) -> APIResponse:
        product = self.service.get_product(product_id)
        if not product:
            raise ProductNotFoundException()
        return APIResponse.ok(data=product, message="Product retrieved successfully")

    def list_products(self, skip: int = 0, limit: int = 100) -> APIResponse:
        products = self.service.get_all_products(skip=skip, limit=limit)
        return APIResponse.ok(data=products, message="Products retrieved successfully")

    def update_product(self, product_id: UUID, payload: ProductCreateRequest) -> APIResponse:
        product = self.service.update_product(
            product_id=product_id,
            name=payload.name,
            sku=payload.sku,
            price=payload.price,
            quantity=payload.quantity
        )
        return APIResponse.ok(data=product, message="Product updated successfully")

    def delete_product(self, product_id: UUID) -> APIResponse:
        self.service.delete_product(product_id)
        return APIResponse.ok(message="Product deleted successfully")
