"""
Strategy module for the Pro Agent.

This module handles prompt building and response parsing,
implementing the debate strategy for the PRO side.
"""

import os
import re
from typing import List, Dict, Any
from pathlib import Path
from dotenv import load_dotenv
from loguru import logger

from debate_day.protocol import Role, MessageType

# Load environment variables
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

# Configuration
AGENT_NAME = os.getenv("AGENT_NAME", "Ava")
ROLE = os.getenv("ROLE", "pro")


def build_prompt(messages: List[Dict[str, Any]]) -> str:
    """
    Build a prompt for the language model based on the debate history.
    
    Args:
        messages: List of message dictionaries from the debate
        
    Returns:
        Formatted prompt string
    """
    # Extract the debate topic from the first system message
    topic = "Unknown Topic"
    for msg in messages:
        if msg.get("role") == "system" and msg.get("message_type") == "system":
            topic = msg.get("content", "Unknown Topic")
            break
    
    # Format message history
    formatted_messages = []
    current_round = 0
    
    # Group messages by round for better readability
    messages_by_round = {}
    for msg in messages:
        round_num = msg.get("round", 0)
        if round_num not in messages_by_round:
            messages_by_round[round_num] = []
        messages_by_round[round_num].append(msg)
    
    # Determine current round based on the last message
    if messages:
        current_round = max(msg.get("round", 0) for msg in messages)
    
    # Format messages by round
    for round_num in sorted(messages_by_round.keys()):
        if round_num > 0:
            formatted_messages.append(f"\n--- Round {round_num} ---\n")
        
        for msg in messages_by_round[round_num]:
            # Skip system messages in the history display
            if msg.get("role") == "system":
                continue
                
            # Format role nicely
            role_display = "Pro" if msg.get("role") == "pro" else "Con" if msg.get("role") == "con" else "Moderator"
            formatted_messages.append(f"{role_display}: {msg.get('content', '')}")
    
    # Create instructions based on the current round
    instructions = ""
    if current_round == 0:
        instructions = (
            "You are arguing IN FAVOR of the topic. "
            "Provide your initial argument in 2-3 sentences. "
            "Be clear, concise, and persuasive. "
            "Focus on your strongest points without attacking the opposing side yet."
        )
    else:
        instructions = (
            "You are arguing IN FAVOR of the topic. "
            f"This is round {current_round}. "
            "Respond to the Con's most recent point with a focused rebuttal. "
            "Be concise and persuasive. "
            "You may acknowledge valid points but reinforce why your position is stronger overall."
        )
    
    # Assemble the final prompt with clear formatting
    prompt = f"""# Debate Topic: {topic}

## Debate History:
{chr(10).join(formatted_messages)}

## Instructions:
You are {AGENT_NAME}, arguing on the PRO side of this debate.
{instructions}

Respond with ONLY your argument text - no explanations, no role-playing, and no meta-commentary.

<response>
"""
    
    return prompt


def parse_response(raw_response: str) -> str:
    """
    Parse and clean the raw response from the language model.
    
    Args:
        raw_response: Raw text from the language model
        
    Returns:
        Cleaned response suitable for sending to the debate
    """
    # Remove any "role playing" or meta instructions
    text = re.sub(r'^\s*\w+:\s*', '', raw_response)  # Remove "Pro:" or similar prefixes
    
    # Remove response tags if present
    text = re.sub(r'<\/?response>', '', text)
    
    # Remove any explanatory notes about the agent's reasoning process
    text = re.sub(r'I am arguing in favor of.*?[\.\n]', '', text)
    text = re.sub(r'As the PRO side.*?[\.\n]', '', text)
    text = re.sub(r'As a proponent.*?[\.\n]', '', text)
    
    # Ensure there are no markdown artifacts
    text = re.sub(r'#+ ', '', text)
    text = re.sub(r'\*\*?(.*?)\*\*?', r'\1', text)
    
    # Clean up extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Ensure the message isn't too long (trimming if necessary)
    max_length = 500
    if len(text) > max_length:
        logger.warning(f"Response exceeds {max_length} characters, trimming...")
        text = text[:max_length].rstrip() + "..."
    
    return text 