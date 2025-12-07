# appV2/schemas/wishlist.py
import uuid
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class AddToWishlistRequest(BaseModel):
    product_id: uuid.UUID
    notes: Optional[str] = None

    model_config = ConfigDict(
        ser_json_timedelta="iso8601", ser_json_bytes="utf8"  # optional extras
    )


class WishlistItemResponse(BaseModel):
    id: uuid.UUID
    product_id: uuid.UUID
    product_name: str
    product_code: str
    product_image: Optional[str] = None
    product_price: float
    notes: Optional[str] = None
    added_at: datetime

    model_config = ConfigDict(from_attributes=True)


class WishlistResponse(BaseModel):
    items: List[WishlistItemResponse]
    total_items: int
