"""
Database models for the MCP server.

This module defines the Pydantic models that represent the internal
data structures used by the MCP server.
"""

from datetime import datetime
from typing import Optional, Dict, Any, List
from enum import Enum
from pydantic import BaseModel, Field, ConfigDict

from debate_day.protocol import Role, MessageType


class SessionStatus(str, Enum):
    """Status of a debate session."""
    PENDING = "pending"
    ACTIVE = "active" 
    FINISHED = "finished"
    ERROR = "error"


class DebateSession(BaseModel):
    """
    Represents a full debate instance.
    
    This model tracks the core metadata about a debate, including its
    current status, configuration, and timing information.
    """
    debate_id: str = Field(..., description="Unique identifier for the debate")
    topic: str = Field(..., description="The topic being debated")
    num_rounds: int = Field(..., description="Maximum number of rounds in the debate")
    created_at: datetime = Field(
        default_factory=datetime.now,
        description="When the debate was created"
    )
    status: SessionStatus = Field(
        default=SessionStatus.PENDING,
        description="Current status of the debate"
    )
    
    # Optional additional fields
    updated_at: Optional[datetime] = Field(
        default=None,
        description="When the debate was last updated"
    )
    finished_at: Optional[datetime] = Field(
        default=None,
        description="When the debate was completed"
    )
    winner: Optional[Role] = Field(
        default=None,
        description="The declared winner of the debate (if finished)"
    )
    
    model_config = ConfigDict(from_attributes=True)


class AgentTurn(BaseModel):
    """
    Represents who is allowed to speak in the current round.
    
    This model tracks the current state of a debate in terms of
    which agent should speak next.
    """
    debate_id: str = Field(..., description="ID of the debate")
    current_round: int = Field(0, description="Current round number")
    next_speaker: Role = Field(..., description="Role that should speak next")
    
    # Additional context fields
    last_message_id: Optional[str] = Field(
        default=None,
        description="ID of the last message in the debate"
    )
    is_final_turn: bool = Field(
        default=False,
        description="Whether this is the final turn (moderator verdict)"
    )
    
    model_config = ConfigDict(from_attributes=True)


class MCPMessageRecord(BaseModel):
    """
    A model that mirrors the MCPMessage, but with additional metadata for DB storage.
    
    This extends the basic MCPMessage with fields needed for database storage
    and retrieval.
    """
    # Core fields from MCPMessage
    debate_id: str = Field(..., description="ID of the debate this message belongs to")
    sender: str = Field(..., description="Identifier of the sender")
    role: Role = Field(..., description="Role of the sender")
    round: int = Field(..., description="Round number")
    content: str = Field(..., description="Message content")
    
    # Additional fields for storage
    message_id: str = Field(..., description="Unique identifier for this message")
    message_type: MessageType = Field(..., description="Type of message")
    timestamp: datetime = Field(
        default_factory=datetime.now,
        description="When the message was created"
    )
    metadata: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="Additional message metadata"
    )
    
    # Database-specific fields
    db_id: Optional[int] = Field(
        default=None,
        description="Database ID (for future persistence)"
    )
    
    model_config = ConfigDict(from_attributes=True)


class DebateSessionWithMessages(DebateSession):
    """Extended DebateSession that includes the full message history."""
    
    messages: List[MCPMessageRecord] = Field(
        default_factory=list,
        description="All messages in the debate"
    )


# Request and response models
class CreateDebateRequest(BaseModel):
    """Request model for creating a new debate."""
    topic: str = Field(..., description="The topic to debate")
    num_rounds: int = Field(1, description="Number of rounds (default: 1)")
    debate_id: Optional[str] = Field(None, description="Custom debate ID (auto-generated if not provided)")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "topic": "Artificial intelligence will benefit humanity more than it will harm it.",
                "num_rounds": 2,
                "debate_id": "custom-debate-123"
            }
        }
    )


class CreateDebateResponse(BaseModel):
    """Response model for debate creation."""
    debate_id: str
    topic: str
    num_rounds: int
    status: SessionStatus
    created_at: datetime


class AddMessageRequest(BaseModel):
    """Request model for adding a message to a debate."""
    sender: str = Field(..., description="Identifier of the sender")
    role: Role = Field(..., description="Role of the sender")
    content: str = Field(..., description="Message content")
    metadata: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Additional message metadata"
    )
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "sender": "ava",
                "role": "pro",
                "content": "AI will revolutionize healthcare and improve patient outcomes globally.",
                "metadata": {"confidence": 0.95}
            }
        }
    )


class DebateStatusResponse(BaseModel):
    """Response model for debate status."""
    debate_id: str
    topic: str
    status: SessionStatus
    current_round: int
    next_speaker: Optional[Role] = None
    message_count: int
    winner: Optional[Role] = None 