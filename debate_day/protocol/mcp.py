"""
Model Context Protocol (MCP) implementation for debate agents.

This module defines a standardized protocol for debate agents to communicate,
ensuring consistent message formats and structured data exchange.
"""

import json
from enum import Enum
from typing import Dict, List, Optional, Any, Union

class MessageType(Enum):
    """Defines the types of messages that can be exchanged between debate agents."""
    ARGUMENT = "argument"
    COUNTER_ARGUMENT = "counter_argument"
    REBUTTAL = "rebuttal"
    EVALUATION = "evaluation"
    TOPIC = "topic"
    RESULT = "result"
    ERROR = "error"

class DebateProtocol:
    """Implements the Model Context Protocol for debate agents."""
    
    @staticmethod
    def format_message(
        message_type: MessageType,
        content: str,
        metadata: Optional[Dict[str, Any]] = None,
        round_number: Optional[int] = None,
        agent_id: Optional[str] = None,
        side: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Format a message according to the protocol.
        
        Args:
            message_type: The type of message being sent
            content: The actual content of the message
            metadata: Additional information about the message
            round_number: Which debate round this message belongs to
            agent_id: Identifier for the agent sending the message
            side: Which side (pro/con) the agent represents
            
        Returns:
            A formatted message dictionary
        """
        message = {
            "type": message_type.value,
            "content": content,
            "metadata": metadata or {},
        }
        
        if round_number is not None:
            message["round"] = round_number
            
        if agent_id is not None:
            message["agent_id"] = agent_id
            
        if side is not None:
            message["side"] = side
            
        return message
    
    @staticmethod
    def parse_message(message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse a message received through the protocol.
        
        Args:
            message: The received message dictionary
            
        Returns:
            A parsed message with validated structure
            
        Raises:
            ValueError: If the message doesn't follow the protocol
        """
        if not isinstance(message, dict):
            raise ValueError("Message must be a dictionary")
            
        if "type" not in message:
            raise ValueError("Message must contain a 'type' field")
            
        if "content" not in message:
            raise ValueError("Message must contain a 'content' field")
            
        try:
            # Validate message type
            message_type = MessageType(message["type"])
        except ValueError:
            valid_types = [t.value for t in MessageType]
            raise ValueError(f"Invalid message type. Must be one of: {valid_types}")
            
        # Create a validated copy of the message
        validated = {
            "type": message_type.value,
            "content": message["content"],
            "metadata": message.get("metadata", {}),
        }
        
        # Copy optional fields if present
        for field in ["round", "agent_id", "side"]:
            if field in message:
                validated[field] = message[field]
                
        return validated

    @staticmethod
    def topic_message(topic: str) -> Dict[str, Any]:
        """Create a formatted topic message."""
        return DebateProtocol.format_message(
            MessageType.TOPIC,
            topic,
            metadata={"description": "Debate topic"}
        )
    
    @staticmethod
    def argument_message(content: str, side: str, agent_id: str, round_number: int = 0) -> Dict[str, Any]:
        """Create a formatted argument message."""
        return DebateProtocol.format_message(
            MessageType.ARGUMENT if round_number == 0 else MessageType.REBUTTAL,
            content,
            metadata={"type": "initial" if round_number == 0 else f"rebuttal_{round_number}"},
            round_number=round_number,
            agent_id=agent_id,
            side=side
        )
    
    @staticmethod
    def evaluation_message(content: str, winner: str, agent_id: str) -> Dict[str, Any]:
        """Create a formatted evaluation message."""
        return DebateProtocol.format_message(
            MessageType.EVALUATION,
            content,
            metadata={"winner": winner},
            agent_id=agent_id
        )
    
    @staticmethod
    def result_message(result: Dict[str, Any]) -> Dict[str, Any]:
        """Create a formatted result message."""
        # Create a JSON-safe copy of the result dictionary
        json_safe_result = {}
        
        for key, value in result.items():
            try:
                # Test if the value is JSON serializable
                json.dumps(value)
                json_safe_result[key] = value
            except (TypeError, OverflowError):
                # If not serializable, convert to string
                json_safe_result[key] = str(value)
        
        return DebateProtocol.format_message(
            MessageType.RESULT,
            json.dumps(json_safe_result),
            metadata={"format": "json"}
        )
    
    @staticmethod
    def error_message(error_message: str, error_code: Optional[str] = None) -> Dict[str, Any]:
        """Create a formatted error message."""
        return DebateProtocol.format_message(
            MessageType.ERROR,
            error_message,
            metadata={"error_code": error_code or "UNKNOWN_ERROR"}
        )

class DebateContext:
    """Manages the context for a debate session."""
    
    def __init__(self, topic: str):
        self.topic = topic
        self.messages: List[Dict[str, Any]] = []
        self.current_round = 0
        self.max_rounds = 0
        
    def add_message(self, message: Dict[str, Any]) -> None:
        """Add a message to the debate context."""
        validated = DebateProtocol.parse_message(message)
        self.messages.append(validated)
        
        # Update current round if needed
        if "round" in validated and validated["round"] > self.current_round:
            self.current_round = validated["round"]
    
    def get_messages_for_round(self, round_number: int) -> List[Dict[str, Any]]:
        """Get all messages for a specific round."""
        return [msg for msg in self.messages if msg.get("round") == round_number]
    
    def get_messages_by_type(self, message_type: MessageType) -> List[Dict[str, Any]]:
        """Get all messages of a specific type."""
        return [msg for msg in self.messages if msg["type"] == message_type.value]
    
    def get_messages_for_agent(self, agent_id: str) -> List[Dict[str, Any]]:
        """Get all messages from a specific agent."""
        return [msg for msg in self.messages if msg.get("agent_id") == agent_id]
    
    def get_messages_for_side(self, side: str) -> List[Dict[str, Any]]:
        """Get all messages from a specific side (pro/con)."""
        return [msg for msg in self.messages if msg.get("side") == side]
    
    def get_latest_message(self, message_type: Optional[MessageType] = None) -> Optional[Dict[str, Any]]:
        """Get the most recent message, optionally filtered by type."""
        if not self.messages:
            return None
            
        if message_type is None:
            return self.messages[-1]
            
        for msg in reversed(self.messages):
            if msg["type"] == message_type.value:
                return msg
                
        return None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the debate context to a dictionary."""
        return {
            "topic": self.topic,
            "messages": self.messages,
            "current_round": self.current_round,
            "max_rounds": self.max_rounds
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DebateContext':
        """Create a debate context from a dictionary."""
        context = cls(data["topic"])
        context.messages = data["messages"]
        context.current_round = data["current_round"]
        context.max_rounds = data["max_rounds"]
        return context 