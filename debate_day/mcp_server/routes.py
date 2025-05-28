"""
API routes for the Debate Day MCP server.

This module defines the FastAPI endpoints for debate management,
message handling, and turn tracking.
"""

from typing import List, Optional, Dict, Any
from fastapi import APIRouter, HTTPException, status, Depends, Query, Path

from debate_day.mcp_server.models import (
    CreateDebateRequest,
    CreateDebateResponse,
    AddMessageRequest,
    DebateStatusResponse,
    MCPMessageRecord,
    AgentTurn,
    SessionStatus,
    DebateSession
)

from debate_day.protocol import (
    MCPMessage,
    Role,
    MessageType,
    generate_debate_id,
    generate_message_id,
    create_system_message
)

from debate_day.mcp_server import db

# Define API router
router = APIRouter(prefix="/api", tags=["debate"])


# --- Helper Functions ---

def _determine_next_speaker(debate_id: str, current_round: int, current_role: Role) -> Role:
    """
    Determine which role should speak next based on current state.
    
    Args:
        debate_id: ID of the debate
        current_round: Current round number
        current_role: Current role that just spoke
        
    Returns:
        Next role that should speak
    """
    debate = db.get_debate(debate_id)
    if not debate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Debate with ID {debate_id} not found"
        )
    
    # Sequence: PRO -> CON -> (next round or MOD)
    if current_role == Role.PRO:
        # After PRO speaks, CON always goes next
        return Role.CON
    elif current_role == Role.CON:
        # After CON speaks in round 0, either go to round 1 or to MOD
        if current_round == 0:
            # If no additional rounds, go to moderator
            if debate.num_rounds == 0:
                return Role.MOD
            # Otherwise start round 1 with PRO
            return Role.PRO
        # After CON speaks in last round, go to moderator
        elif current_round >= debate.num_rounds:
            return Role.MOD
        # Otherwise continue to next round
        else:
            return Role.PRO
    elif current_role == Role.MOD:
        # After moderator speaks, debate is over
        return None
    
    # Default (start of debate) is PRO
    return Role.PRO


def _update_debate_status_after_message(debate_id: str, message: MCPMessageRecord) -> None:
    """
    Update debate status and turn after a new message.
    
    Args:
        debate_id: ID of the debate
        message: The message that was just added
    """
    debate = db.get_debate(debate_id)
    if not debate:
        return
    
    # Determine next speaker
    current_round = message.round
    next_round = current_round
    
    # If CON just spoke and it's not the final round, increment round
    if message.role == Role.CON and current_round < debate.num_rounds:
        next_round = current_round + 1
    
    # If MOD just spoke, debate is finished
    if message.role == Role.MOD:
        db.update_debate_status(debate_id, SessionStatus.FINISHED)
        
        # Check for winner in metadata
        if message.metadata and "winner" in message.metadata:
            winner_role = message.metadata["winner"]
            db.set_debate_winner(debate_id, winner_role)
        
        # No next turn after moderator
        return
    
    # Determine who speaks next
    next_speaker = _determine_next_speaker(debate_id, current_round, message.role)
    
    # If no next speaker, debate is finished
    if next_speaker is None:
        db.update_debate_status(debate_id, SessionStatus.FINISHED)
        return
    
    # Update the current turn
    turn = AgentTurn(
        debate_id=debate_id,
        current_round=next_round,
        next_speaker=next_speaker,
        last_message_id=message.message_id,
        is_final_turn=(next_speaker == Role.MOD)
    )
    db.set_agent_turn(turn)
    
    # If debate was pending, mark it as active
    if debate.status == SessionStatus.PENDING:
        db.update_debate_status(debate_id, SessionStatus.ACTIVE)


# --- API Endpoints ---

@router.post("/start", response_model=CreateDebateResponse, status_code=status.HTTP_201_CREATED)
async def start_debate(request: CreateDebateRequest) -> CreateDebateResponse:
    """
    Create a new debate session.
    
    Args:
        request: The debate creation request
        
    Returns:
        New debate session information
    """
    # Generate a unique debate ID
    debate_id = generate_debate_id()
    
    # Create the debate session
    debate = DebateSession(
        debate_id=debate_id,
        topic=request.topic,
        num_rounds=request.num_rounds,
        status=SessionStatus.PENDING
    )
    
    # Store the debate
    db.create_debate(debate)
    
    # Create initial system message with the topic
    system_message = MCPMessageRecord(
        debate_id=debate_id,
        message_id=generate_message_id(),
        sender="system",
        role="system",
        round=0,
        content=request.topic,
        message_type=MessageType.SYSTEM,
        metadata={"type": "topic"}
    )
    db.save_message(system_message)
    
    # Set initial turn (PRO goes first)
    initial_turn = AgentTurn(
        debate_id=debate_id,
        current_round=0,
        next_speaker=Role.PRO
    )
    db.set_agent_turn(initial_turn)
    
    # Return the debate information
    return CreateDebateResponse(
        debate_id=debate_id,
        topic=request.topic,
        num_rounds=request.num_rounds,
        status=SessionStatus.PENDING,
        created_at=debate.created_at
    )


@router.post("/message/{debate_id}", status_code=status.HTTP_200_OK)
async def add_message(
    debate_id: str = Path(..., description="ID of the debate"),
    request: AddMessageRequest = None
) -> Dict[str, Any]:
    """
    Add a message to a debate.
    
    Args:
        debate_id: ID of the debate
        request: The message to add
        
    Returns:
        Status information
    """
    # Check if debate exists
    debate = db.get_debate(debate_id)
    if not debate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Debate with ID {debate_id} not found"
        )
    
    # Check if debate is finished
    if debate.status == SessionStatus.FINISHED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot add messages to a finished debate"
        )
    
    # Check if it's the sender's turn
    turn = db.get_agent_turn(debate_id)
    if not turn or turn.next_speaker != request.role:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"It's not {request.role}'s turn to speak"
        )
    
    # Determine message type based on role and round
    message_type = MessageType.ARGUMENT
    if request.role == Role.MOD:
        message_type = MessageType.VERDICT
    elif turn.current_round > 0:
        message_type = MessageType.REBUTTAL
    elif request.role == Role.CON:
        message_type = MessageType.COUNTER
    
    # Create the message record
    message = MCPMessageRecord(
        debate_id=debate_id,
        message_id=generate_message_id(),
        sender=request.sender,
        role=request.role,
        round=turn.current_round,
        content=request.content,
        message_type=message_type,
        metadata=request.metadata or {}
    )
    
    # Save the message
    db.save_message(message)
    
    # Update debate status and turn
    _update_debate_status_after_message(debate_id, message)
    
    # Return success
    return {
        "status": "success",
        "message_id": message.message_id,
        "debate_id": debate_id
    }


@router.get("/context/{debate_id}", response_model=List[Dict[str, Any]])
async def get_context(
    debate_id: str = Path(..., description="ID of the debate"),
    limit: int = Query(10, description="Maximum number of messages to return")
) -> List[Dict[str, Any]]:
    """
    Get the context (previous messages) for a debate.
    
    Args:
        debate_id: ID of the debate
        limit: Maximum number of messages to return
        
    Returns:
        List of messages
    """
    # Check if debate exists
    if not db.get_debate(debate_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Debate with ID {debate_id} not found"
        )
    
    # Get messages
    messages = db.get_messages(debate_id)
    
    # Apply limit if needed
    if limit and limit < len(messages):
        messages = messages[-limit:]
    
    # Convert to dictionary representation
    return [message.dict() for message in messages]


@router.get("/turn/{debate_id}")
async def get_turn(debate_id: str = Path(..., description="ID of the debate")) -> Dict[str, Any]:
    """
    Get information about whose turn it is in a debate.
    
    Args:
        debate_id: ID of the debate
        
    Returns:
        Turn information
    """
    # Check if debate exists
    debate = db.get_debate(debate_id)
    if not debate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Debate with ID {debate_id} not found"
        )
    
    # Get turn information
    turn = db.get_agent_turn(debate_id)
    if not turn:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No turn information available for this debate"
        )
    
    # Return turn information
    return {
        "debate_id": debate_id,
        "current_round": turn.current_round,
        "next_speaker": turn.next_speaker,
        "is_final_turn": turn.is_final_turn,
        "status": debate.status
    }


@router.get("/status/{debate_id}", response_model=DebateStatusResponse)
async def get_status(debate_id: str = Path(..., description="ID of the debate")) -> DebateStatusResponse:
    """
    Get the current status of a debate.
    
    Args:
        debate_id: ID of the debate
        
    Returns:
        Debate status information
    """
    # Check if debate exists
    debate = db.get_debate(debate_id)
    if not debate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Debate with ID {debate_id} not found"
        )
    
    # Get turn information
    turn = db.get_agent_turn(debate_id)
    
    # Count messages
    message_count = db.count_messages(debate_id)
    
    # Return status information
    return DebateStatusResponse(
        debate_id=debate_id,
        topic=debate.topic,
        status=debate.status,
        current_round=turn.current_round if turn else 0,
        next_speaker=turn.next_speaker if turn else None,
        message_count=message_count,
        winner=debate.winner
    )


@router.get("/debates", response_model=List[Dict[str, Any]])
async def list_debates() -> List[Dict[str, Any]]:
    """
    List all available debates.
    
    Returns:
        List of debate information
    """
    debates = db.list_debates()
    return [
        {
            "debate_id": debate.debate_id,
            "topic": debate.topic,
            "status": debate.status,
            "num_rounds": debate.num_rounds,
            "created_at": debate.created_at,
            "winner": debate.winner
        }
        for debate in debates
    ]


@router.get("/debate/{debate_id}", response_model=Dict[str, Any])
async def get_debate(debate_id: str = Path(..., description="ID of the debate")) -> Dict[str, Any]:
    """
    Get detailed information about a debate.
    
    Args:
        debate_id: ID of the debate
        
    Returns:
        Complete debate information including messages
    """
    # Get debate with messages
    debate_data = db.get_debate_with_messages(debate_id)
    if not debate_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Debate with ID {debate_id} not found"
        )
    
    # Convert to dictionary representation
    return {
        "debate": debate_data["debate"].dict(),
        "messages": [msg.dict() for msg in debate_data["messages"]],
        "current_turn": debate_data["current_turn"].dict() if debate_data["current_turn"] else None
    }


def get_router():
    """Get the API router."""
    return router 