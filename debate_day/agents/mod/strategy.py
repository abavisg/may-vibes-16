"""
Strategy module for the Moderator Agent.

This module handles prompt building and response parsing,
implementing the debate strategy for the MODERATOR role.
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
AGENT_NAME = os.getenv("AGENT_NAME", "Mia")
ROLE = os.getenv("ROLE", "mod")


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
    
    # Count arguments from each side for analysis
    pro_messages = []
    con_messages = []
    
    # Group messages by round for better readability
    messages_by_round = {}
    for msg in messages:
        # Collect pro and con messages for analysis
        if msg.get("role") == "pro":
            pro_messages.append(msg)
        elif msg.get("role") == "con":
            con_messages.append(msg)
            
        round_num = msg.get("round", 0)
        if round_num not in messages_by_round:
            messages_by_round[round_num] = []
        messages_by_round[round_num].append(msg)
    
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
    
    # Create comprehensive instructions for verdict
    instructions = (
        "You are the MODERATOR of this debate. "
        "Your role is to carefully evaluate the arguments presented by both sides and render a verdict. "
        f"The Pro side ({pro_messages[0].get('sender', 'Pro') if pro_messages else 'Pro'}) has argued FOR the topic. "
        f"The Con side ({con_messages[0].get('sender', 'Con') if con_messages else 'Con'}) has argued AGAINST the topic. "
        "\n\n"
        "In your evaluation, consider the following criteria:\n"
        "1. Strength and coherence of arguments\n"
        "2. Quality of evidence and reasoning\n"
        "3. Effectiveness of rebuttals\n"
        "4. Overall persuasiveness\n"
        "\n"
        "You MUST explicitly declare a winner by stating one of these phrases in your verdict:\n"
        "- 'I declare PRO as the winner.'\n"
        "- 'I declare CON as the winner.'\n"
        "\n"
        "Provide a brief justification for your decision. Be fair and impartial in your assessment."
    )
    
    # Assemble the final prompt with clear formatting
    prompt = f"""# Debate Topic: {topic}

## Debate History:
{chr(10).join(formatted_messages)}

## Instructions:
You are {AGENT_NAME}, the moderator of this debate.
{instructions}

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
    text = re.sub(r'^\s*\w+:\s*', '', raw_response)  # Remove "Moderator:" or similar prefixes
    
    # Remove response tags if present
    text = re.sub(r'<\/?response>', '', text)
    
    # Ensure there are no markdown artifacts
    text = re.sub(r'#+ ', '', text)
    text = re.sub(r'\*\*?(.*?)\*\*?', r'\1', text)
    
    # Clean up extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    # If the verdict doesn't explicitly state a winner, try to add it
    if not any(phrase in text.lower() for phrase in ["declare pro", "declare con", "pro as the winner", "con as the winner"]):
        pro_indicators = ["pro made the stronger case", "pro side was more persuasive", "pro had better arguments"]
        con_indicators = ["con made the stronger case", "con side was more persuasive", "con had better arguments"]
        
        pro_match = any(indicator in text.lower() for indicator in pro_indicators)
        con_match = any(indicator in text.lower() for indicator in con_indicators)
        
        if pro_match and not con_match:
            text += " I declare PRO as the winner."
        elif con_match and not pro_match:
            text += " I declare CON as the winner."
    
    # Ensure the message isn't too long (trimming if necessary)
    max_length = 1000  # Allowing longer response for the verdict
    if len(text) > max_length:
        logger.warning(f"Response exceeds {max_length} characters, trimming...")
        # Try to find a sentence boundary for cleaner trimming
        last_period = text[:max_length].rfind('.')
        if last_period > max_length * 0.75:  # Ensure we don't trim too much
            text = text[:last_period+1]
        else:
            text = text[:max_length].rstrip() + "..."
    
    return text 