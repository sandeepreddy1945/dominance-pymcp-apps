# appV2/schemas/cart.py
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, ConfigDict


class AddToCartRequest(BaseModel):
    product_id: uuid.UUID
    quantity: int = Field(default=1, ge=1, le=100)
    product_options: Optional[Dict[str, Any]] = None


class UpdateCartItemRequest(BaseModel):
    quantity: int = Field(ge=1, le=100)


class CartItemResponse(BaseModel):
    id: uuid.UUID
    product_id: uuid.UUID
    product_name: str
    product_code: str
    product_image: Optional[str] = None
    quantity: int
    unit_price: float
    total_price: float
    product_options: Dict[str, Any] = {}
    added_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CartResponse(BaseModel):
    items: List[CartItemResponse]
    total_items: int
    total_amount: float
    currency: str = "USD"


class SavedItemResponse(BaseModel):
    id: uuid.UUID
    product_id: uuid.UUID
    product_name: str
    product_code: str
    product_image: Optional[str] = None
    unit_price: float
    saved_at: datetime

    model_config = ConfigDict(from_attributes=True)
