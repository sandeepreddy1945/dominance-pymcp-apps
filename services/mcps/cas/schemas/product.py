import uuid
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict


class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    category: Optional[str] = None
    price: float
    currency: str = "USD"


class ProductResponse(BaseModel):
    id: uuid.UUID
    code: str
    name: str
    description: Optional[str] = None
    category: Optional[str] = None
    price: float
    currency: str
    image_url: Optional[str] = None
    in_stock: bool
    custom_fields: Dict[str, Any] = {}

    model_config = ConfigDict(from_attributes=True)


class ProductSearchResponse(BaseModel):
    products: List[ProductResponse]
    total: int
    query: str
    filters: Dict[str, Any]
