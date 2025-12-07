# appV2/schemas/conversation.py - Enhanced with context data

import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict


class ConversationCreate(BaseModel):
    title: Optional[str] = None
    language: str = "en"


class ConversationResponse(BaseModel):
    id: uuid.UUID
    title: str
    language: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class MessageCreate(BaseModel):
    content: str
    message_type: str = "text"


class EnhancedMessageResponse(BaseModel):
    """Enhanced message response with full context and UI data"""

    id: uuid.UUID
    role: str
    content: str
    message_type: str

    # Core AI data
    intent: Optional[str] = None
    entities: Dict[str, Any] = {}
    confidence_score: Optional[float] = None
    tool_calls: List[str] = []

    # Enhanced context data
    context_memory: Dict[str, Any] = {}
    resolved_references: Dict[str, Any] = {}
    tool_results: Dict[str, Any] = {}
    session_data: Dict[str, Any] = {}

    # UI-specific data
    response_type: str = "text"
    ui_components: Dict[str, Any] = {}
    user_preferences_snapshot: Dict[str, Any] = {}

    # Error handling
    has_error: bool = False
    error_message: Optional[str] = None

    # Metadata
    processing_time_ms: Optional[int] = None
    model_version: Optional[str] = None
    conversation_turn: Optional[int] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class MessageResponse(BaseModel):
    """Backward compatible message response"""

    id: uuid.UUID
    role: str
    content: str
    intent: Optional[str] = None
    entities: Dict[str, Any] = {}
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[uuid.UUID] = None
    language: str = "en"


class EnhancedChatResponse(BaseModel):
    """Enhanced chat response with full context"""

    success: bool
    response: str
    response_type: str

    # AI processing data
    intent: Optional[str] = None
    entities: Dict[str, Any] = {}
    confidence_score: Optional[float] = None

    # Context and memory
    context_memory: Dict[str, Any] = {}
    resolved_references: Dict[str, Any] = {}
    tool_results: Dict[str, Any] = {}
    session_data: Dict[str, Any] = {}

    # UI data for consistent display
    ui_components: Dict[str, Any] = {}

    # Conversation metadata
    conversation_id: uuid.UUID
    conversation_turn: Optional[int] = None

    # Error handling
    error: Optional[str] = None
    has_error: bool = False

    # Performance metrics
    processing_time_ms: Optional[int] = None
    model_version: str = "claude-3-sonnet"


class ChatResponse(BaseModel):
    """Backward compatible chat response"""

    success: bool
    response: str
    response_type: str
    intent: Optional[str] = None
    entities: Dict[str, Any] = {}
    tool_results: Dict[str, Any] = {}
    conversation_id: uuid.UUID
    error: Optional[str] = None


class ConversationSummary(BaseModel):
    """Summary of conversation with key metrics"""

    id: uuid.UUID
    title: str
    language: str
    message_count: int
    last_intent: Optional[str] = None
    last_response_type: Optional[str] = None
    created_at: datetime
    last_message_at: datetime
    is_active: bool

    # Summary metrics
    total_tools_used: int
    unique_intents: List[str]
    has_errors: bool

    model_config = ConfigDict(from_attributes=True)


class ConversationAnalytics(BaseModel):
    """Analytics data for a conversation"""

    conversation_id: uuid.UUID
    total_messages: int
    user_messages: int
    assistant_messages: int

    # Intent distribution
    intent_distribution: Dict[str, int]

    # Tool usage
    tool_usage: Dict[str, int]
    successful_tools: int
    failed_tools: int

    # Response types
    response_type_distribution: Dict[str, int]

    # Performance metrics
    average_processing_time: Optional[float]
    total_processing_time: Optional[int]

    # Error metrics
    total_errors: int
    error_rate: float

    # Context usage
    context_references_used: int
    memory_references: int

    model_config = ConfigDict(from_attributes=True)


class MessageSearchRequest(BaseModel):
    """Request for searching messages"""

    conversation_id: Optional[uuid.UUID] = None
    query: Optional[str] = None
    intent: Optional[str] = None
    response_type: Optional[str] = None
    has_error: Optional[bool] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    limit: int = 50
    offset: int = 0


class MessageSearchResponse(BaseModel):
    """Response for message search"""

    messages: List[EnhancedMessageResponse]
    total_count: int
    search_query: str
    filters_applied: Dict[str, Any]

    model_config = ConfigDict(from_attributes=True)


class ContextSnapshot(BaseModel):
    """Snapshot of conversation context at a point in time"""

    conversation_id: uuid.UUID
    message_id: uuid.UUID
    snapshot_time: datetime

    # Context data
    context_memory: Dict[str, Any]
    resolved_references: Dict[str, Any]
    session_data: Dict[str, Any]
    user_preferences: Dict[str, Any]

    # Summary
    intent_at_time: Optional[str]
    entities_at_time: Dict[str, Any]
    tools_executed: List[str]

    model_config = ConfigDict(from_attributes=True)


class UIComponentData(BaseModel):
    """Structured UI component data for different response types"""

    component_type: str  # product_list, cart_summary, order_confirmation, etc.
    data: Dict[str, Any]
    display_options: Dict[str, Any] = {}
    actions_available: List[str] = []

    model_config = ConfigDict(from_attributes=True)
