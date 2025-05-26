"""
Protocol package for standardizing agent communication in the debate system.
"""

from .mcp import (
    MessageType,
    DebateProtocol,
    DebateContext
)

__all__ = [
    "MessageType",
    "DebateProtocol",
    "DebateContext"
] 