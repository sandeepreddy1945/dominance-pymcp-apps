import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, EmailStr, ConfigDict


class UTCBaseModel(BaseModel):
    model_config = ConfigDict(
        json_encoders={datetime: lambda v: v.astimezone(timezone.utc).isoformat()}
    )


class UserBase(UTCBaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    locale: str = "en"
    interests: List[str] = []
    preferences: Dict[str, Any] = {}


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    locale: Optional[str] = None
    interests: Optional[List[str]] = None
    preferences: Optional[Dict[str, Any]] = None
    avatar_url: Optional[str] = None


class UserResponse(UserBase):
    id: uuid.UUID
    is_active: bool
    is_superuser: bool
    avatar_url: Optional[str] = None
    created_at: datetime
    last_active: datetime

    model_config = ConfigDict(from_attributes=True)


class UserLogin(BaseModel):
    username: str
    password: str


# Role and Permission schemas
class PermissionOut(BaseModel):
    id: int
    name: str
    description: Optional[str]

    model_config = ConfigDict(from_attributes=True)


class RoleOut(BaseModel):
    id: int
    name: str
    description: Optional[str]
    permissions: List[PermissionOut]

    model_config = ConfigDict(from_attributes=True)


# Other related models (minimal)
class ConversationOut(BaseModel):
    id: uuid.UUID

    # Add relevant fields here
    model_config = ConfigDict(from_attributes=True)


class OrderOut(BaseModel):
    id: uuid.UUID

    # Add relevant fields here
    model_config = ConfigDict(from_attributes=True)


class CartItemOut(BaseModel):
    id: uuid.UUID

    # Add relevant fields here
    model_config = ConfigDict(from_attributes=True)


class ProductViewOut(UTCBaseModel):
    id: uuid.UUID
    product_id: uuid.UUID
    viewed_at: datetime

    model_config = ConfigDict(from_attributes=True)


# Extended User Response
class UserFullResponse(UserResponse):
    roles: Optional[List[RoleOut]] = None
    conversations: Optional[List[ConversationOut]] = None
    orders: Optional[List[OrderOut]] = None
    cart_items: Optional[List[CartItemOut]] = None
    viewed_products: Optional[List[ProductViewOut]] = None


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserFullResponse
