from uuid import UUID
from typing import List, Optional
from app.models.customer import Customer
from app.repository.customer.repository import CustomerRepositoryInterface
from app.interfaces.customer import CustomerServiceInterface

from app.utils.exceptions import CustomerNotFoundException, ConflictException

class CustomerService(CustomerServiceInterface):
    def __init__(self, repository: CustomerRepositoryInterface):
        self.repository = repository

    def get_customer(self, customer_id: UUID) -> Optional[Customer]:
        return self.repository.get_by_id(customer_id)

    def get_customer_by_email(self, email: str) -> Optional[Customer]:
        return self.repository.get_by_email(email)

    def get_all_customers(self, skip: int = 0, limit: int = 100) -> List[Customer]:
        return self.repository.get_all(skip=skip, limit=limit)

    def register_customer(self, first_name: str, last_name: str, email: str, phone_number: Optional[str] = None) -> Customer:
        if self.repository.get_by_email(email):
            raise ConflictException("Customer email already registered.")
        return self.repository.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number
        )

    def delete_customer(self, customer_id: UUID) -> None:
        if not self.repository.get_by_id(customer_id):
            raise CustomerNotFoundException()
        self.repository.delete(customer_id)
