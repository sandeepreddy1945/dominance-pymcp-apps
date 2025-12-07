# appV2/schemas/admin.py
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, validator, ConfigDict

# ==================== COMMON SCHEMAS ====================


class PaginatedResponse(BaseModel):
    """Base schema for paginated responses"""

    total_count: int
    skip: int
    limit: int
    has_next: bool
    has_previous: bool

    @validator("has_next", pre=True, always=True)
    def calculate_has_next(cls, v, values):
        total = values.get("total_count", 0)
        skip = values.get("skip", 0)
        limit = values.get("limit", 0)
        return skip + limit < total

    @validator("has_previous", pre=True, always=True)
    def calculate_has_previous(cls, v, values):
        skip = values.get("skip", 0)
        return skip > 0


class BulkOperationRequest(BaseModel):
    """Schema for bulk operations"""

    item_ids: List[uuid.UUID]
    action: str
    parameters: Optional[Dict[str, Any]] = {}


class BulkOperationResponse(BaseModel):
    """Response for bulk operations"""

    success: bool
    affected_count: int
    failed_count: Optional[int] = 0
    message: str
    errors: Optional[List[str]] = []


# ==================== DASHBOARD SCHEMAS ====================


class DashboardOverview(BaseModel):
    """Dashboard overview statistics"""

    total_users: int
    total_products: int
    total_orders: int
    total_revenue: float
    active_conversations: int
    open_tickets: int


class UserMetrics(BaseModel):
    """User-related metrics"""

    total: int
    active: int
    inactive: int
    new_today: int
    new_this_week: int


class ProductMetrics(BaseModel):
    """Product-related metrics"""

    total: int
    active: int
    inactive: int
    out_of_stock: int
    low_stock: int


class OrderMetrics(BaseModel):
    """Order-related metrics"""

    total: int
    pending: int
    completed: int
    today: int
    completion_rate: float


class RevenueMetrics(BaseModel):
    """Revenue-related metrics"""

    total: float
    today: float
    this_week: float
    average_order_value: float


class ConversationMetrics(BaseModel):
    """Conversation-related metrics"""

    total: int
    active: int
    today: int


class SupportMetrics(BaseModel):
    """Support ticket metrics"""

    total_tickets: int
    open_tickets: int
    urgent_tickets: int


class CartMetrics(BaseModel):
    """Shopping cart metrics"""

    active_carts: int
    total_items: int
    average_items_per_cart: float


class TopProduct(BaseModel):
    """Top selling product"""

    name: str
    total_sold: int


class DashboardResponse(BaseModel):
    """Complete dashboard response"""

    overview: DashboardOverview
    users: UserMetrics
    products: ProductMetrics
    orders: OrderMetrics
    revenue: RevenueMetrics
    conversations: ConversationMetrics
    support: SupportMetrics
    cart: CartMetrics
    top_products: List[TopProduct]


# ==================== ANALYTICS SCHEMAS ====================


class TrendDataPoint(BaseModel):
    """Single data point for trend analytics"""

    date: str
    count: int


class OrderTrendDataPoint(BaseModel):
    """Order trend data point with revenue"""

    date: str
    order_count: int
    revenue: float


class AnalyticsTrendsResponse(BaseModel):
    """Analytics trends response"""

    period_days: int
    user_registrations: List[TrendDataPoint]
    daily_orders: List[OrderTrendDataPoint]
    daily_conversations: List[TrendDataPoint]


class DistributionItem(BaseModel):
    """Distribution data item"""

    label: str
    count: int


class AnalyticsDistribution(BaseModel):
    """Analytics distribution data"""

    status_distribution: List[DistributionItem]
    category_distribution: List[DistributionItem]
    priority_distribution: List[DistributionItem]


# ==================== USER MANAGEMENT SCHEMAS ====================


class AdminUserResponse(BaseModel):
    """Enhanced user response for admin"""

    id: str
    username: str
    email: str
    full_name: Optional[str]
    is_active: bool
    is_superuser: bool
    locale: str
    interests: List[str]
    preferences: Dict[str, Any]
    avatar_url: Optional[str]
    created_at: datetime
    last_active: datetime
    roles: List[str]
    total_orders: int
    total_conversations: int

    model_config = ConfigDict(from_attributes=True) 


class UserListResponse(PaginatedResponse):
    """Paginated user list response"""

    users: List[AdminUserResponse]
    filters: Dict[str, Any]


class UserStatistics(BaseModel):
    """User statistics"""

    total_orders: int
    total_conversations: int
    cart_items: int
    products_viewed: int
    total_spent: float
    average_order_value: float


class RecentOrder(BaseModel):
    """Recent order summary"""

    id: str
    status: str
    total_amount: float
    created_at: datetime


class RecentConversation(BaseModel):
    """Recent conversation summary"""

    id: str
    title: Optional[str]
    is_active: bool
    created_at: datetime
    last_message_at: datetime


class UserDetailsResponse(BaseModel):
    """Detailed user information"""

    user: AdminUserResponse
    statistics: UserStatistics
    recent_orders: List[RecentOrder]
    recent_conversations: List[RecentConversation]


class UserCreateRequest(BaseModel):
    """Create user request"""

    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., pattern=r"^[^@]+@[^@]+\.[^@]+$")
    password: str = Field(..., min_length=8)
    full_name: Optional[str] = Field(None, max_length=100)
    locale: str = Field(default="en", pattern="^(en|fr)$")
    interests: List[str] = Field(default=[])
    preferences: Dict[str, Any] = Field(default={})


class UserUpdateRequest(BaseModel):
    """Update user request"""

    full_name: Optional[str] = Field(None, max_length=100)
    locale: Optional[str] = Field(None, pattern="^(en|fr)$")
    interests: Optional[List[str]] = None
    preferences: Optional[Dict[str, Any]] = None
    avatar_url: Optional[str] = None
    is_active: Optional[bool] = None


# ==================== PRODUCT MANAGEMENT SCHEMAS ====================


class AdminProductResponse(BaseModel):
    """Enhanced product response for admin"""

    id: str
    code: str
    name: str
    name_en: str
    name_fr: Optional[str]
    description: Optional[str]
    description_en: Optional[str]
    description_fr: Optional[str]
    category: Optional[str]
    category_en: Optional[str]
    category_fr: Optional[str]
    price: float
    currency: str
    image_url: Optional[str]
    images: List[str]
    is_active: bool
    is_embedding_generated: bool
    in_stock: bool
    stock_quantity: int
    custom_fields: Dict[str, Any]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ProductListResponse(PaginatedResponse):
    """Paginated product list response"""

    products: List[AdminProductResponse]
    filters: Dict[str, Any]


class ProductStatistics(BaseModel):
    """Product statistics"""

    total_views: int
    total_cart_adds: int
    total_orders: int
    total_sold: int
    total_revenue: float
    conversion_rate: float


class ProductActivity(BaseModel):
    """Product activity data"""

    user_id: str
    viewed_at: datetime
    session_id: Optional[str]


class ProductDetailsResponse(BaseModel):
    """Detailed product information"""

    product: AdminProductResponse
    statistics: ProductStatistics
    recent_activity: Dict[str, List[ProductActivity]]


class ProductCreateRequest(BaseModel):
    """Create product request"""

    code: str = Field(..., min_length=1, max_length=50)
    name_en: str = Field(..., min_length=1, max_length=200)
    name_fr: Optional[str] = Field(None, max_length=200)
    description_en: Optional[str] = None
    description_fr: Optional[str] = None
    summary_en: Optional[str] = None
    summary_fr: Optional[str] = None
    combined_detail_en: Optional[str] = None
    price: float = Field(..., ge=0)
    currency: str = Field(default="USD", max_length=3)
    category_en: Optional[str] = Field(None, max_length=100)
    category_fr: Optional[str] = Field(None, max_length=100)
    image_url: Optional[str] = None
    images: List[str] = Field(default=[])
    is_active: bool = Field(default=True)
    in_stock: bool = Field(default=True)
    stock_quantity: int = Field(default=0, ge=0)
    custom_fields: Dict[str, Any] = Field(default={})


class ProductUpdateRequest(BaseModel):
    """Update product request"""

    name_en: Optional[str] = Field(None, min_length=1, max_length=200)
    name_fr: Optional[str] = Field(None, max_length=200)
    description_en: Optional[str] = None
    description_fr: Optional[str] = None
    summary_en: Optional[str] = None
    summary_fr: Optional[str] = None
    combined_detail_en: Optional[str] = None
    price: Optional[float] = Field(None, ge=0)
    currency: Optional[str] = Field(None, max_length=3)
    category_en: Optional[str] = Field(None, max_length=100)
    category_fr: Optional[str] = Field(None, max_length=100)
    image_url: Optional[str] = None
    images: Optional[List[str]] = None
    is_active: Optional[bool] = None
    in_stock: Optional[bool] = None
    stock_quantity: Optional[int] = Field(None, ge=0)
    custom_fields: Optional[Dict[str, Any]] = None


class StockUpdateRequest(BaseModel):
    """Stock update request"""

    action: str = Field(..., pattern="^(set|add|subtract)$")
    quantity: int = Field(..., ge=0)


class BulkPriceUpdateRequest(BaseModel):
    """Bulk price update request"""

    product_ids: List[uuid.UUID]
    action: str = Field(..., pattern="^(set|increase|decrease)$")
    value: float = Field(..., ge=0)
    percentage: bool = Field(default=False)


# ==================== ORDER MANAGEMENT SCHEMAS ====================


class AdminOrderItemResponse(BaseModel):
    """Order item response for admin"""

    id: str
    product_id: str
    product_name: str
    product_code: str
    quantity: int
    unit_price: float
    total_price: float
    product_options: Dict[str, Any]
    product: Optional[Dict[str, Any]] = None

    model_config = ConfigDict(from_attributes=True)


class AdminOrderResponse(BaseModel):
    """Enhanced order response for admin"""

    id: str
    user: Optional[Dict[str, Any]]
    status: str
    total_amount: float
    currency: str
    payment_method: str
    payment_status: str
    payment_details: Dict[str, Any]
    shipping_address: Dict[str, Any]
    shipping_method: str
    shipping_cost: float
    order_notes: Optional[str]
    created_at: datetime
    updated_at: datetime
    shipped_at: Optional[datetime]
    delivered_at: Optional[datetime]
    item_count: int
    items: List[AdminOrderItemResponse]

    model_config = ConfigDict(from_attributes=True)


class OrderListResponse(PaginatedResponse):
    """Paginated order list response"""

    orders: List[AdminOrderResponse]
    filters: Dict[str, Any]


class OrderStatusHistory(BaseModel):
    """Order status history"""

    id: str
    old_status: Optional[str]
    new_status: str
    notes: Optional[str]
    changed_by: Optional[str]
    created_at: datetime


class OrderDetailsResponse(BaseModel):
    """Detailed order information"""

    order: AdminOrderResponse
    items: List[AdminOrderItemResponse]
    status_history: List[OrderStatusHistory]


class OrderStatusUpdateRequest(BaseModel):
    """Order status update request"""

    new_status: str = Field(
        ...,
        pattern="^(pending|confirmed|processing|shipped|delivered|cancelled|refunded)$",
    )
    notes: Optional[str] = Field(None, max_length=500)


class PaymentStatusUpdateRequest(BaseModel):
    """Payment status update request"""

    payment_status: str = Field(
        ..., pattern="^(pending|processing|completed|failed|refunded|cancelled)$"
    )
    payment_details: Optional[Dict[str, Any]] = None


class OrderUpdateRequest(BaseModel):
    """Order update request"""

    shipping_address: Optional[Dict[str, Any]] = None
    shipping_method: Optional[str] = None
    shipping_cost: Optional[float] = Field(None, ge=0)
    order_notes: Optional[str] = None
    payment_method: Optional[str] = None


class RefundRequest(BaseModel):
    """Refund request"""

    amount: Optional[float] = Field(None, ge=0)
    reason: str = Field(..., min_length=1, max_length=500)


# ==================== CONVERSATION MANAGEMENT SCHEMAS ====================


class AdminConversationResponse(BaseModel):
    """Enhanced conversation response for admin"""

    id: str
    user: Optional[Dict[str, Any]]
    title: Optional[str]
    language: str
    current_intent: Optional[str]
    context_data: Dict[str, Any]
    user_preferences: Dict[str, Any]
    is_active: bool
    is_completed: bool
    created_at: datetime
    updated_at: datetime
    last_message_at: datetime
    message_count: int
    user_message_count: int
    assistant_message_count: int

    model_config = ConfigDict(from_attributes=True)


class ConversationListResponse(PaginatedResponse):
    """Paginated conversation list response"""

    conversations: List[AdminConversationResponse]


class ConversationMessageResponse(BaseModel):
    """Conversation message response"""

    id: str
    role: str
    content: str
    message_type: str
    intent: Optional[str]
    entities: Dict[str, Any]
    confidence_score: Optional[float]
    tool_calls: List[str]
    context_memory: Dict[str, Any]
    resolved_references: Dict[str, Any]
    tool_results: Dict[str, Any]
    session_data: Dict[str, Any]
    response_type: str
    ui_components: Dict[str, Any]
    user_preferences_snapshot: Dict[str, Any]
    has_error: bool
    error_message: Optional[str]
    processing_time_ms: Optional[int]
    model_version: Optional[str]
    conversation_turn: Optional[int]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ConversationAnalytics(BaseModel):
    """Conversation analytics"""

    total_messages: int
    user_messages: int
    assistant_messages: int
    unique_intents: List[str]
    intent_distribution: Dict[str, int]
    response_type_distribution: Dict[str, int]
    error_count: int
    error_rate: float
    average_processing_time: float


class ConversationDetailsResponse(BaseModel):
    """Detailed conversation information"""

    conversation: AdminConversationResponse
    messages: Optional[List[ConversationMessageResponse]] = None
    analytics: Optional[ConversationAnalytics] = None


class ConversationUpdateRequest(BaseModel):
    """Conversation update request"""

    title: Optional[str] = Field(None, max_length=200)
    language: Optional[str] = Field(None, pattern="^(en|fr)$")
    current_intent: Optional[str] = None
    context_data: Optional[Dict[str, Any]] = None
    user_preferences: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None
    is_completed: Optional[bool] = None


# ==================== SUPPORT TICKET SCHEMAS ====================


class AdminSupportTicketResponse(BaseModel):
    """Enhanced support ticket response for admin"""

    id: str
    user: Optional[Dict[str, Any]]
    subject: str
    description: str
    category: Optional[str]
    priority: str
    status: str
    order_id: Optional[str]
    conversation_id: Optional[str]
    assigned_to: Optional[str]
    created_at: datetime
    updated_at: datetime
    resolved_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)


class SupportTicketListResponse(PaginatedResponse):
    """Paginated support ticket list response"""

    tickets: List[AdminSupportTicketResponse]
    filters: Dict[str, Any]


class SupportTicketDetailsResponse(BaseModel):
    """Detailed support ticket information"""

    ticket: AdminSupportTicketResponse
    related_order: Optional[Dict[str, Any]] = None
    related_conversation: Optional[Dict[str, Any]] = None


class SupportTicketCreateRequest(BaseModel):
    """Create support ticket request"""

    user_id: uuid.UUID
    subject: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=10, max_length=2000)
    category: Optional[str] = Field(
        None,
        pattern="^(technical|billing|shipping|product|account|general|refund|complaint)$",
    )
    priority: str = Field(default="medium", pattern="^(low|medium|high|urgent)$")
    order_id: Optional[uuid.UUID] = None
    conversation_id: Optional[uuid.UUID] = None


class SupportTicketUpdateRequest(BaseModel):
    """Update support ticket request"""

    subject: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, min_length=10, max_length=2000)
    category: Optional[str] = Field(
        None,
        pattern="^(technical|billing|shipping|product|account|general|refund|complaint)$",
    )
    priority: Optional[str] = Field(None, pattern="^(low|medium|high|urgent)$")
    status: Optional[str] = Field(None, pattern="^(open|in_progress|resolved|closed)$")
    assigned_to: Optional[str] = None


class TicketAssignmentRequest(BaseModel):
    """Ticket assignment request"""

    assigned_to: str = Field(..., min_length=1, max_length=100)


class TicketResolutionRequest(BaseModel):
    """Ticket resolution request"""

    resolution_notes: str = Field(..., min_length=1, max_length=1000)


# ==================== CART MANAGEMENT SCHEMAS ====================


class AdminCartItemResponse(BaseModel):
    """Cart item response for admin"""

    id: str
    product: Optional[Dict[str, Any]]
    quantity: int
    unit_price: float
    total_price: float
    added_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AdminCartResponse(BaseModel):
    """Cart response for admin"""

    user: Optional[Dict[str, Any]]
    item_count: int
    total_value: float
    last_updated: datetime
    items: List[AdminCartItemResponse]

    model_config = ConfigDict(from_attributes=True)


class CartListResponse(PaginatedResponse):
    """Paginated cart list response"""

    carts: List[AdminCartResponse]


class CartAnalytics(BaseModel):
    """Cart analytics"""

    overview: Dict[str, Any]
    popular_cart_items: List[Dict[str, Any]]


# ==================== SYSTEM SCHEMAS ====================


class ProductFieldConfig(BaseModel):
    """Product field configuration"""

    id: int
    field_name: str
    field_type: str
    is_required: bool
    default_value: Optional[str]
    validation_rules: Dict[str, Any]
    is_searchable: bool

    model_config = ConfigDict(from_attributes=True)


class SystemSettingsResponse(BaseModel):
    """System settings response"""

    product_fields: List[ProductFieldConfig]


class ProductFieldCreateRequest(BaseModel):
    """Create product field request"""

    field_name: str = Field(..., min_length=1, max_length=50)
    field_type: str = Field(..., pattern="^(string|integer|float|boolean|json)$")
    is_required: bool = Field(default=False)
    default_value: Optional[str] = None
    validation_rules: Dict[str, Any] = Field(default={})
    is_searchable: bool = Field(default=False)


# ==================== EXPORT SCHEMAS ====================


class ExportRequest(BaseModel):
    """Export request"""

    format: str = Field(..., pattern="^(csv|json|xlsx)$")
    filters: Optional[Dict[str, Any]] = None
    fields: Optional[List[str]] = None


class ExportResponse(BaseModel):
    """Export response"""

    download_url: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
    exported_at: datetime
    record_count: int


# ==================== SEARCH & FILTER SCHEMAS ====================


class SearchRequest(BaseModel):
    """Generic search request"""

    query: Optional[str] = None
    filters: Dict[str, Any] = Field(default={})
    sort_by: str = Field(default="created_at")
    sort_order: str = Field(default="desc", pattern="^(asc|desc)$")
    skip: int = Field(default=0, ge=0)
    limit: int = Field(default=100, ge=1, le=1000)


class FilterOption(BaseModel):
    """Filter option"""

    value: str
    label: str
    count: Optional[int] = None


class SearchFilters(BaseModel):
    """Available search filters"""

    categories: List[FilterOption]
    statuses: List[FilterOption]
    priorities: List[FilterOption]
    languages: List[FilterOption]
