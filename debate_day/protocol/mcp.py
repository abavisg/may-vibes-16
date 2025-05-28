"""
Model Context Protocol (MCP) for Debate Day 2.0

This module defines the message protocol that serves as the shared contract
between all components of the Debate Day system.
"""

from enum import Enum
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class Role(str, Enum):
    """Agent roles in the debate system."""
    PRO = "pro"
    CON = "con"
    MOD = "mod"


class MessageType(str, Enum):
    """Types of messages that can be exchanged in a debate."""
    ARGUMENT = "argument"       # Initial position statement
    REBUTTAL = "rebuttal"       # Response to previous arguments
    COUNTER = "counter"         # Direct challenge to opponent's point
    VERDICT = "verdict"         # Final judgment from moderator
    SYSTEM = "system"           # System messages (debate start/end)
    ERROR = "error"             # Error messages
    
    
class DebateStatus(str, Enum):
    """Possible states of a debate session."""
    INITIALIZED = "initialized"  # Debate created but not started
    IN_PROGRESS = "in_progress"  # Debate is ongoing
    COMPLETED = "completed"      # Debate has concluded
    ERROR = "error"              # Debate encountered an error


class MCPMessage(BaseModel):
    """
    Standard message format for all communication in the Debate Day system.
    
    This model defines the structure that all messages must follow, whether
    they are sent by agents, the MCP server, or CLI tools.
    """
    # Required fields
    debate_id: str = Field(..., description="Unique identifier for the debate")
    sender: str = Field(..., description="Identifier of the sender (e.g., 'pro', 'con', 'mod', 'system')")
    role: Role = Field(..., description="Role of the sender in the debate")
    round: int = Field(..., description="Round number in the debate (0 = initial arguments)")
    content: str = Field(..., description="Actual message content")
    
    # Optional fields
    message_id: Optional[str] = Field(None, description="Unique identifier for this message")
    message_type: Optional[MessageType] = Field(None, description="Type of message being sent")
    timestamp: Optional[str] = Field(
        default_factory=lambda: datetime.now().isoformat(),
        description="When the message was created"
    )
    metadata: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="Additional data about the message (e.g., model, tokens)"
    )
    
    model_config = ConfigDict(use_enum_values=True)


class PromptFormatter:
    """
    Utilities for formatting debate history into LLM prompts.
    
    This class provides methods to convert MCP messages into formatted
    text suitable for prompting language models.
    """
    
    @staticmethod
    def format_debate_history(messages: List[MCPMessage], include_rounds: bool = True) -> str:
        """
        Format a list of MCP messages into a readable debate history.
        
        Args:
            messages: List of MCPMessage objects
            include_rounds: Whether to include round numbers
            
        Returns:
            Formatted debate history as a string
        """
        if not messages:
            return ""
        
        formatted_messages = []
        
        # Group messages by round for better readability
        messages_by_round = {}
        for msg in messages:
            if msg.round not in messages_by_round:
                messages_by_round[msg.round] = []
            messages_by_round[msg.round].append(msg)
        
        # Format each round
        for round_num in sorted(messages_by_round.keys()):
            if include_rounds and round_num > 0:
                formatted_messages.append(f"\n--- Round {round_num} ---\n")
            
            # Format messages in this round
            for msg in messages_by_round[round_num]:
                role_display = "Pro" if msg.role == Role.PRO else "Con" if msg.role == Role.CON else "Moderator"
                formatted_messages.append(f"{role_display}: {msg.content}")
        
        return "\n\n".join(formatted_messages)
    
    @staticmethod
    def format_for_agent(
        role: Role, 
        messages: List[MCPMessage],
        current_round: int
    ) -> str:
        """
        Format debate history specifically for an agent's prompt.
        
        Args:
            role: Which role this prompt is for
            messages: List of debate messages
            current_round: The current round number
            
        Returns:
            Formatted prompt text
        """
        # Get the debate topic (assuming it's in the first system message)
        topic = "Unknown Topic"
        for msg in messages:
            if msg.sender == "system" and msg.round == 0:
                topic = msg.content
                break
        
        # Format the debate history
        history = PromptFormatter.format_debate_history(messages)
        
        # Create a role-specific prompt
        if role == Role.PRO:
            if current_round == 0:
                instruction = (
                    f"You are arguing IN FAVOR of the topic. "
                    f"Provide your initial argument in 1-2 sentences."
                )
            else:
                instruction = (
                    f"You are arguing IN FAVOR of the topic. "
                    f"This is round {current_round}. "
                    f"Respond to the Con's most recent point with a focused rebuttal."
                )
        elif role == Role.CON:
            if current_round == 0:
                instruction = (
                    f"You are arguing AGAINST the topic. "
                    f"Provide your initial counter-argument in 1-2 sentences."
                )
            else:
                instruction = (
                    f"You are arguing AGAINST the topic. "
                    f"This is round {current_round}. "
                    f"Respond to the Pro's most recent point with a focused rebuttal."
                )
        elif role == Role.MOD:
            instruction = (
                f"You are the MODERATOR of this debate. "
                f"Review the arguments from both sides and declare a winner "
                f"based on the strength of their reasoning and evidence."
            )
        else:
            instruction = "Review the debate history and respond appropriately."
        
        # Assemble the final prompt
        prompt = f"""
Topic: {topic}

Debate History:
{history}

{instruction}
"""
        return prompt.strip()


def validate_message(message: Dict[str, Any]) -> MCPMessage:
    """
    Validate a message dictionary against the MCP protocol.
    
    Args:
        message: Dictionary representation of a message
        
    Returns:
        Validated MCPMessage object
        
    Raises:
        ValueError: If the message is invalid
    """
    try:
        return MCPMessage(**message)
    except Exception as e:
        raise ValueError(f"Invalid MCP message format: {e}")
    

def create_system_message(
    debate_id: str,
    content: str,
    round: int = 0,
    message_type: MessageType = MessageType.SYSTEM
) -> MCPMessage:
    """
    Create a system message.
    
    Args:
        debate_id: ID of the debate
        content: Message content
        round: Debate round
        message_type: Type of message
        
    Returns:
        MCPMessage object
    """
    return MCPMessage(
        debate_id=debate_id,
        sender="system",
        role="system",  # Using string instead of enum since "system" isn't in Role
        round=round,
        content=content,
        message_type=message_type,
        metadata={"system": True}
    ) 