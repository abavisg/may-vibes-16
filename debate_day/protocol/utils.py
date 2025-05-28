"""
Utility functions for the Model Context Protocol.

This module provides helper functions for working with MCP messages.
"""

import uuid
import json
from typing import List, Dict, Any, Optional
from datetime import datetime

from .mcp import MCPMessage, Role, MessageType


def generate_message_id() -> str:
    """
    Generate a unique message ID.
    
    Returns:
        Unique ID string
    """
    return str(uuid.uuid4())


def generate_debate_id() -> str:
    """
    Generate a unique debate ID.
    
    Returns:
        Unique ID string
    """
    return str(uuid.uuid4())


def create_agent_message(
    debate_id: str,
    content: str,
    sender: str,
    role: Role,
    round_num: int,
    message_type: Optional[MessageType] = None
) -> MCPMessage:
    """
    Create a message from an agent.
    
    Args:
        debate_id: ID of the debate
        content: Message content
        sender: Agent identifier
        role: Agent role
        round_num: Current round number
        message_type: Optional message type
        
    Returns:
        MCPMessage object
    """
    # Determine message type if not provided
    if message_type is None:
        if round_num == 0:
            message_type = MessageType.ARGUMENT
        else:
            message_type = MessageType.REBUTTAL
            
        # Special case for moderator
        if role == Role.MOD:
            message_type = MessageType.VERDICT
    
    return MCPMessage(
        debate_id=debate_id,
        message_id=generate_message_id(),
        sender=sender,
        role=role,
        round=round_num,
        content=content,
        message_type=message_type,
        timestamp=datetime.now().isoformat(),
        metadata={
            "timestamp_unix": datetime.now().timestamp()
        }
    )


def format_debate_for_export(messages: List[MCPMessage], topic: str) -> Dict[str, Any]:
    """
    Format a debate for export to JSON.
    
    Args:
        messages: List of debate messages
        topic: Debate topic
        
    Returns:
        Dictionary representation of the debate
    """
    # Group messages by round
    rounds = {}
    for msg in messages:
        if msg.round not in rounds:
            rounds[msg.round] = []
        rounds[msg.round].append(msg.dict())
    
    # Get winner from moderator verdict (if available)
    winner = None
    for msg in messages:
        if msg.role == Role.MOD and msg.message_type == MessageType.VERDICT:
            # Check metadata for winner
            if msg.metadata and "winner" in msg.metadata:
                winner = msg.metadata["winner"]
    
    # Format the debate
    return {
        "topic": topic,
        "timestamp": datetime.now().isoformat(),
        "rounds": rounds,
        "num_messages": len(messages),
        "winner": winner,
        "full_history": [msg.dict() for msg in messages]
    }


def serialize_to_json(data: Any) -> str:
    """
    Serialize data to JSON.
    
    Args:
        data: Data to serialize
        
    Returns:
        JSON string
    """
    return json.dumps(data, indent=2, sort_keys=True)


def save_debate_to_file(
    messages: List[MCPMessage],
    topic: str,
    file_path: str
) -> bool:
    """
    Save a debate to a JSON file.
    
    Args:
        messages: List of debate messages
        topic: Debate topic
        file_path: Path to save the file
        
    Returns:
        True if successful, False otherwise
    """
    try:
        debate_data = format_debate_for_export(messages, topic)
        with open(file_path, 'w') as f:
            f.write(serialize_to_json(debate_data))
        return True
    except Exception as e:
        print(f"Error saving debate: {e}")
        return False


def extract_topic_from_messages(messages: List[MCPMessage]) -> str:
    """
    Extract the debate topic from a list of messages.
    
    Args:
        messages: List of MCPMessage objects
        
    Returns:
        Debate topic string
    """
    # Look for system messages with the topic
    for msg in messages:
        if msg.sender == "system" and msg.round == 0:
            return msg.content
    
    # If no system message found, return a default
    return "Unknown Topic" 