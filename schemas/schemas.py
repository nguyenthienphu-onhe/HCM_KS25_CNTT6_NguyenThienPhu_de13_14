from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Any
from datetime import datetime

class StandardResponse(BaseModel):
    statusCode: int
    error: Optional[str] = None
    message: str
    data: Any = None

# Danh Mục
class CategoryResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    model_config = ConfigDict(from_attributes=True)

#Sản Phẩm
class ProductCreate(BaseModel):
    product_code: str = Field(..., min_length=4, max_length=10)
    name: str = Field(..., min_length=2, max_length=100)
    price: float = Field(..., gt=0)
    stock_quantity: int = Field(..., ge=0)
    category_id: int

class ProductUpdate(BaseModel):
    price: Optional[float] = Field(None, gt=0)
    stock_quantity: Optional[int] = Field(None, ge=0)

class ProductResponse(BaseModel):
    id: int
    product_code: str
    name: str
    price: float
    stock_quantity: int
    category: Optional[CategoryResponse] = None
    model_config = ConfigDict(from_attributes=True)

class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0)

class OrderCreate(BaseModel):
    customer_name: str = Field(..., min_length=1)
    items: List[OrderItemCreate] = Field(..., min_length=1)

class OrderItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    unit_price: float
    product: Optional[ProductResponse] = None
    model_config = ConfigDict(from_attributes=True)

class OrderResponse(BaseModel):
    id: int
    order_code: str
    customer_name: str
    total_amount: float
    status: str
    created_at: datetime
    items: List[OrderItemResponse] = []
    model_config = ConfigDict(from_attributes=True)