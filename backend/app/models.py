from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class QueryRequest(BaseModel):
    """Request model for chat queries"""
    query: str = Field(
        ..., 
        min_length=1, 
        max_length=1000,
        description="User question or query",
        example="What documents do I need to travel from Kenya to Ireland?"
    )
    user_id: Optional[str] = Field(
        None,
        description="Optional user identifier for history tracking"
    )

class QueryResponse(BaseModel):
    """Response model for chat queries"""
    id: Optional[int] = Field(None, description="Query ID")
    query: str = Field(..., description="Original user query")
    response: str = Field(..., description="AI-generated response")
    timestamp: datetime = Field(..., description="Response timestamp")
    response_time: Optional[float] = Field(None, description="Response time in seconds")
    success: bool = Field(True, description="Whether the query was successful")

class ErrorResponse(BaseModel):
    """Error response model"""
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Human-readable error message")
    detail: Optional[str] = Field(None, description="Detailed error information")

class HealthResponse(BaseModel):
    """Health check response model"""
    status: str = Field(..., description="Service status")
    message: str = Field(..., description="Status message")
    timestamp: datetime = Field(default_factory=datetime.now)

class QueryHistoryResponse(BaseModel):
    """Response model for query history"""
    queries: List[QueryResponse] = Field(..., description="List of previous queries")
    total_count: int = Field(..., description="Total number of queries")
    page: int = Field(1, description="Current page number")
    page_size: int = Field(10, description="Number of items per page")

class QueryStatus(str, Enum):
    """Enum for query status"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

# Database models (for SQLAlchemy)
class QueryRecord:
    """Database record for storing queries"""
    def __init__(self, query: str, response: str, user_id: Optional[str] = None):
        self.query = query
        self.response = response
        self.user_id = user_id
        self.timestamp = datetime.now()
        self.success = True