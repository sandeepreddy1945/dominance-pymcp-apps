import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, ConfigDict


class OrderItemResponse(BaseModel):
    id: uuid.UUID
    product_id: uuid.UUID
    product_name: str
    product_code: str
    quantity: int
    unit_price: float
    total_price: float

    model_config = ConfigDict(from_attributes=True)


class OrderResponse(BaseModel):
    id: uuid.UUID
    status: str
    total_amount: float
    currency: str
    payment_method: str
    payment_status: str
    shipping_address: Dict[str, Any]
    created_at: datetime
    items: List[OrderItemResponse]

    model_config = ConfigDict(from_attributes=True)


class CheckoutRequest(BaseModel):
    conversation_id: Optional[uuid.UUID] = None
    shipping_address: Optional[Dict[str, Any]] = None
    payment_method: str = "cash_on_delivery"
    order_notes: Optional[str] = None


class OrderStatusUpdate(BaseModel):
    new_status: str
    notes: Optional[str] = None


from uuid import UUID


class QuickOrderRequest(BaseModel):
    product_id: UUID
    quantity: int = Field(default=1, ge=1, le=100)
    shipping_address: Optional[Dict[str, Any]] = None
    payment_method: str = Field(default="cash_on_delivery")
    order_notes: Optional[str] = None


class OrderTrackingResponse(BaseModel):
    order_id: UUID
    current_status: str
    payment_status: str
    estimated_delivery: Optional[datetime]
    tracking_number: Optional[str]
    status_history: List[Dict[str, Any]]

    model_config = ConfigDict(from_attributes=True)


class OrderAnalyticsResponse(BaseModel):
    period: str
    total_orders: int
    total_spent: float
    average_order_value: float
    orders_by_month: List[Dict[str, Any]]
    top_categories: List[Dict[str, Any]]
    spending_trend: List[Dict[str, Any]]


class OrderStatsResponse(BaseModel):
    lifetime_orders: int
    lifetime_spent: float
    average_order_value: float
    favorite_category: Optional[str]
    last_order_date: Optional[datetime]
    pending_orders: int
    completed_orders: int
    cancelled_orders: int
