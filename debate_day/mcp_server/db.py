"""
In-memory database for the MCP server.

This module provides temporary storage for debate sessions, messages,
and turn information during runtime. No persistence is implemented yet.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime

from debate_day.mcp_server.models import (
    DebateSession,
    MCPMessageRecord,
    AgentTurn,
    SessionStatus
)

# In-memory "database" structures
debate_sessions: Dict[str, DebateSession] = {}
debate_messages: Dict[str, List[MCPMessageRecord]] = {}
agent_turns: Dict[str, AgentTurn] = {}

# --- Session Management ---

def create_debate(session: DebateSession) -> None:
    """
    Store a new debate session by ID.
    
    Args:
        session: The debate session to store
    """
    debate_sessions[session.debate_id] = session
    # Initialize empty message list
    debate_messages[session.debate_id] = []

def get_debate(debate_id: str) -> Optional[DebateSession]:
    """
    Retrieve a debate session by ID.
    
    Args:
        debate_id: ID of the debate to retrieve
        
    Returns:
        DebateSession if found, None otherwise
    """
    return debate_sessions.get(debate_id)

def update_debate(session: DebateSession) -> None:
    """
    Update an existing debate session.
    
    Args:
        session: The updated debate session
    """
    if session.debate_id in debate_sessions:
        # Update the timestamp
        session.updated_at = datetime.now()
        debate_sessions[session.debate_id] = session

def list_debates() -> List[DebateSession]:
    """
    List all available debates.
    
    Returns:
        List of all debate sessions
    """
    return list(debate_sessions.values())

def delete_debate(debate_id: str) -> bool:
    """
    Delete a debate session and all associated data.
    
    Args:
        debate_id: ID of the debate to delete
        
    Returns:
        True if deleted, False if not found
    """
    if debate_id in debate_sessions:
        del debate_sessions[debate_id]
        if debate_id in debate_messages:
            del debate_messages[debate_id]
        if debate_id in agent_turns:
            del agent_turns[debate_id]
        return True
    return False

def update_debate_status(debate_id: str, status: SessionStatus) -> bool:
    """
    Update the status of a debate session.
    
    Args:
        debate_id: ID of the debate to update
        status: New status to set
        
    Returns:
        True if updated, False if not found
    """
    if debate_id in debate_sessions:
        debate = debate_sessions[debate_id]
        debate.status = status
        debate.updated_at = datetime.now()
        
        # If finished, set the finished_at timestamp
        if status == SessionStatus.FINISHED:
            debate.finished_at = datetime.now()
            
        debate_sessions[debate_id] = debate
        return True
    return False

def set_debate_winner(debate_id: str, winner_role: str) -> bool:
    """
    Set the winner of a debate.
    
    Args:
        debate_id: ID of the debate
        winner_role: Role of the winning agent
        
    Returns:
        True if updated, False if not found
    """
    if debate_id in debate_sessions:
        debate = debate_sessions[debate_id]
        debate.winner = winner_role
        debate.updated_at = datetime.now()
        debate_sessions[debate_id] = debate
        return True
    return False

# --- Message Handling ---

def save_message(message: MCPMessageRecord) -> None:
    """
    Append a message to the debate's history.
    
    Args:
        message: The message to save
    """
    if message.debate_id not in debate_messages:
        debate_messages[message.debate_id] = []
    debate_messages[message.debate_id].append(message)

def get_messages(debate_id: str) -> List[MCPMessageRecord]:
    """
    Retrieve all messages for a given debate.
    
    Args:
        debate_id: ID of the debate
        
    Returns:
        List of messages in chronological order
    """
    return debate_messages.get(debate_id, [])

def get_latest_message(debate_id: str) -> Optional[MCPMessageRecord]:
    """
    Get the most recent message in a debate.
    
    Args:
        debate_id: ID of the debate
        
    Returns:
        Most recent message or None if no messages
    """
    messages = debate_messages.get(debate_id, [])
    if messages:
        return messages[-1]
    return None

def get_messages_by_round(debate_id: str, round_num: int) -> List[MCPMessageRecord]:
    """
    Get all messages for a specific round in a debate.
    
    Args:
        debate_id: ID of the debate
        round_num: Round number to filter by
        
    Returns:
        List of messages in the specified round
    """
    all_messages = debate_messages.get(debate_id, [])
    return [msg for msg in all_messages if msg.round == round_num]

def get_messages_by_role(debate_id: str, role: str) -> List[MCPMessageRecord]:
    """
    Get all messages from a specific role in a debate.
    
    Args:
        debate_id: ID of the debate
        role: Role to filter by
        
    Returns:
        List of messages from the specified role
    """
    all_messages = debate_messages.get(debate_id, [])
    return [msg for msg in all_messages if msg.role == role]

def count_messages(debate_id: str) -> int:
    """
    Count the number of messages in a debate.
    
    Args:
        debate_id: ID of the debate
        
    Returns:
        Number of messages
    """
    return len(debate_messages.get(debate_id, []))

# --- Agent Turn Tracking ---

def set_agent_turn(turn: AgentTurn) -> None:
    """
    Set whose turn it is for a debate.
    
    Args:
        turn: The turn information to store
    """
    agent_turns[turn.debate_id] = turn

def get_agent_turn(debate_id: str) -> Optional[AgentTurn]:
    """
    Get the current agent turn for a debate.
    
    Args:
        debate_id: ID of the debate
        
    Returns:
        Current turn information or None if not found
    """
    return agent_turns.get(debate_id)

def update_agent_turn(debate_id: str, **kwargs: Any) -> bool:
    """
    Update specific fields of an agent turn.
    
    Args:
        debate_id: ID of the debate
        **kwargs: Fields to update
        
    Returns:
        True if updated, False if not found
    """
    if debate_id in agent_turns:
        turn = agent_turns[debate_id]
        for key, value in kwargs.items():
            if hasattr(turn, key):
                setattr(turn, key, value)
        agent_turns[debate_id] = turn
        return True
    return False

# --- Combined Operations ---

def get_debate_with_messages(debate_id: str) -> Optional[Dict[str, Any]]:
    """
    Get a debate session with all its messages.
    
    Args:
        debate_id: ID of the debate
        
    Returns:
        Dictionary with debate and messages, or None if not found
    """
    debate = get_debate(debate_id)
    if not debate:
        return None
    
    messages = get_messages(debate_id)
    turn = get_agent_turn(debate_id)
    
    return {
        "debate": debate,
        "messages": messages,
        "current_turn": turn
    }

def clear_all() -> None:
    """Clear all data from the in-memory database."""
    debate_sessions.clear()
    debate_messages.clear()
    agent_turns.clear() 