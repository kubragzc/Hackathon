from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ProductBase(BaseModel):
    name: str
    price: float
    stock: int
    category: str
    producer_member: str

class Product(ProductBase):
    id: int
    class Config:
        from_attributes = True

class CustomerBase(BaseModel):
    name: str
    phone: str
    address: str

class Customer(CustomerBase):
    id: int
    join_date: Optional[datetime] = None
    class Config:
        from_attributes = True

class OrderItem(BaseModel):
    product_id: int
    quantity: int
    price_at_time: float

    class Config:
        from_attributes = True

class Order(BaseModel):
    id: int
    customer_id: int
    order_date: datetime
    status: str
    total_amount: float
    tracking_number: Optional[str] = None
    customer_note: Optional[str] = None
    estimated_delivery: Optional[datetime] = None
    payment_method: Optional[str] = None
    payment_status: Optional[bool] = False
    items: List[OrderItem] = []

    class Config:
        from_attributes = True

class OrderWithCustomer(Order):
    customer: Customer
    
    class Config:
        from_attributes = True
