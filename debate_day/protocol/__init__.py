"""
Protocol package for Debate Day 2.0.

This package contains the Model Context Protocol (MCP) implementation.
"""

from .mcp import (
    MCPMessage,
    Role,
    MessageType,
    DebateStatus,
    PromptFormatter,
    validate_message,
    create_system_message
)

from .utils import (
    generate_message_id,
    generate_debate_id,
    create_agent_message,
    format_debate_for_export,
    serialize_to_json,
    save_debate_to_file,
    extract_topic_from_messages
)

__all__ = [
    # From mcp.py
    'MCPMessage',
    'Role',
    'MessageType',
    'DebateStatus',
    'PromptFormatter',
    'validate_message',
    'create_system_message',
    
    # From utils.py
    'generate_message_id',
    'generate_debate_id',
    'create_agent_message',
    'format_debate_for_export',
    'serialize_to_json',
    'save_debate_to_file',
    'extract_topic_from_messages'
] 