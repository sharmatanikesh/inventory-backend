import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import String, Numeric, Integer, CheckConstraint, Boolean, DateTime, func, Index
from sqlalchemy.orm import Mapped, mapped_column
from app.models.base import Base

class Product(Base):
    __tablename__ = "products"
    
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    sku: Mapped[str] = mapped_column(String(100), nullable=False)
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        onupdate=func.now(), 
        nullable=False
    )
    deleted_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), 
        nullable=True
    )
    
    __table_args__ = (
        CheckConstraint("quantity >= 0", name="check_quantity_non_negative"),
        # Unique constraint on active SKUs only
        Index("idx_products_sku_active", "sku", unique=True, postgresql_where="deleted_at IS NULL"),
    )
