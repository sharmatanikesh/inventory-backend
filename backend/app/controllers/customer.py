from uuid import UUID
from app.interfaces.customer import CustomerServiceInterface
from app.schemas.customer import CustomerCreateRequest
from app.utils.response import APIResponse
from app.utils.exceptions import CustomerNotFoundException

class CustomerController:
    def __init__(self, service: CustomerServiceInterface):
        self.service = service

    def register_customer(self, payload: CustomerCreateRequest) -> APIResponse:
        customer = self.service.register_customer(
            first_name=payload.first_name,
            last_name=payload.last_name,
            email=payload.email,
            phone_number=payload.phone_number
        )
        return APIResponse.ok(data=customer, message="Customer registered successfully")

    def get_customer(self, customer_id: UUID) -> APIResponse:
        customer = self.service.get_customer(customer_id)
        if not customer:
            raise CustomerNotFoundException()
        return APIResponse.ok(data=customer, message="Customer retrieved successfully")

    def list_customers(self, skip: int = 0, limit: int = 100) -> APIResponse:
        customers = self.service.get_all_customers(skip=skip, limit=limit)
        return APIResponse.ok(data=customers, message="Customers retrieved successfully")

    def delete_customer(self, customer_id: UUID) -> APIResponse:
        self.service.delete_customer(customer_id)
        return APIResponse.ok(message="Customer deleted successfully")
