from uuid import UUID
from typing import List, Optional
from app.models.customer import Customer
from app.repository.customer.repository import CustomerRepositoryInterface
from app.repository.user.repository import UserRepositoryInterface
from app.interfaces.customer import CustomerServiceInterface
from app.utils.auth import generate_temp_password, get_password_hash
from app.utils.exceptions import CustomerNotFoundException, ConflictException

class CustomerService(CustomerServiceInterface):
    def __init__(self, repository: CustomerRepositoryInterface, user_repo: UserRepositoryInterface):
        self.repository = repository
        self.user_repo = user_repo

    def get_customer(self, customer_id: UUID) -> Optional[Customer]:
        return self.repository.get_by_id(customer_id)

    def get_customer_by_email(self, email: str) -> Optional[Customer]:
        return self.repository.get_by_email(email)

    def get_all_customers(self, skip: int = 0, limit: int = 100) -> List[Customer]:
        return self.repository.get_all(skip=skip, limit=limit)

    def register_customer(self, first_name: str, last_name: str, email: str, phone_number: Optional[str] = None) -> Customer:
        if self.repository.get_by_email(email) or self.user_repo.get_by_email(email):
            raise ConflictException("Customer email already registered.")
            
        # Generate custom temporary password (first 4 of name + 4 random characters)
        temp_password = generate_temp_password(first_name)
        
        # Create User account
        user = self.user_repo.create(
            email=email,
            password_hash=get_password_hash(temp_password),
            role="CUSTOMER"
        )
        
        # Create Customer profile linked to User
        customer = self.repository.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            user_id=user.id
        )
        
        # Attach password in-memory to be returned to client exactly once
        customer.password = temp_password
        return customer


    def delete_customer(self, customer_id: UUID) -> None:
        if not self.repository.get_by_id(customer_id):
            raise CustomerNotFoundException()
        self.repository.delete(customer_id)
