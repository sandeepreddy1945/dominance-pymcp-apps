# appV2/schemas/support.py
import uuid
from datetime import datetime
from typing import Dict, Optional

from pydantic import BaseModel, Field, ConfigDict


class CreateSupportTicketRequest(BaseModel):
    subject: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=10, max_length=2000)
    category: Optional[str] = Field(
        None,
        pattern="^(technical|billing|shipping|product|account|general|refund|complaint)$",
    )
    priority: str = Field(default="medium", pattern="^(low|medium|high|urgent)$")
    order_id: Optional[uuid.UUID] = None
    conversation_id: Optional[uuid.UUID] = None


class UpdateSupportTicketRequest(BaseModel):
    description: str = Field(..., min_length=10, max_length=2000)


class SupportTicketResponse(BaseModel):
    id: uuid.UUID
    subject: str
    description: str
    category: Optional[str]
    priority: str
    status: str
    order_id: Optional[uuid.UUID]
    conversation_id: Optional[uuid.UUID]
    assigned_to: Optional[str]
    created_at: datetime
    updated_at: datetime
    resolved_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)


class SupportTicketStatsResponse(BaseModel):
    total_tickets: int
    open_tickets: int
    closed_tickets: int
    average_resolution_time: Optional[float]  # in hours
    tickets_by_category: Dict[str, int]
    tickets_by_priority: Dict[str, int]


class TicketMessageResponse(BaseModel):
    id: uuid.UUID
    message: str
    sender_type: str  # user, admin, system
    sender_name: Optional[str]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
