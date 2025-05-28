#!/usr/bin/env python3
"""
Pro Agent for Debate Day 2.0.

This agent participates in debates on the PRO side, using the MCP server
for communication and coordination.
"""

import os
import time
import json
from typing import List, Dict, Any
from pathlib import Path
import httpx
from dotenv import load_dotenv
from loguru import logger

from debate_day.protocol import MCPMessage, Role, MessageType
from debate_day.agents.pro.strategy import build_prompt, parse_response
from debate_day.agents.pro.llm_config import generate_response

# Create logs directory at project root
project_root = Path(__file__).parent.parent.parent.parent # This assumes agents/pro/main.py, so ../../../ is root
logs_dir = project_root / "logs"
logs_dir.mkdir(parents=True, exist_ok=True)

# Configure logging
logger.remove()
logger.add(
    logs_dir / "pro_agent_{time}.log", # Updated path
    rotation="10 MB",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
)
logger.add(lambda msg: print(msg), level="INFO", format="{message}")

# Load environment variables
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

# Configuration
ROLE = os.getenv("ROLE", "pro")
MODEL = os.getenv("MODEL", "llama3")
MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "http://localhost:8000")
AGENT_NAME = os.getenv("AGENT_NAME", "Ava")
DEBATE_ID = os.getenv("DEBATE_ID", "test-debate-id-001")

# Polling interval (seconds)
POLL_INTERVAL = 10


def check_turn() -> bool:
    """
    Check if it's this agent's turn to speak.
    
    Returns:
        True if it's this agent's turn, False otherwise
    """
    try:
        logger.info(f"Checking if it's {ROLE}'s turn...")
        url = f"{MCP_SERVER_URL}/api/turn/{DEBATE_ID}"
        response = httpx.get(url)
        response.raise_for_status()
        
        data = response.json()
        is_our_turn = data.get("next_speaker") == ROLE
        
        if is_our_turn:
            logger.info(f"It's {ROLE}'s turn in round {data.get('current_round')}!")
        else:
            logger.debug(f"Not our turn. Current speaker: {data.get('next_speaker')}")
            
        return is_our_turn
    
    except Exception as e:
        logger.error(f"Error checking turn: {e}")
        return False


def get_context() -> List[Dict[str, Any]]:
    """
    Get the current debate context (message history).
    
    Returns:
        List of message dictionaries
    """
    try:
        logger.info("Fetching debate context...")
        url = f"{MCP_SERVER_URL}/api/context/{DEBATE_ID}"
        response = httpx.get(url)
        response.raise_for_status()
        
        messages = response.json()
        logger.info(f"Fetched {len(messages)} messages from context")
        return messages
    
    except Exception as e:
        logger.error(f"Error fetching context: {e}")
        return []


def send_message(content: str) -> bool:
    """
    Send a message to the debate.
    
    Args:
        content: The message content
        
    Returns:
        True if successful, False otherwise
    """
    try:
        logger.info("Sending message...")
        url = f"{MCP_SERVER_URL}/api/message/{DEBATE_ID}"
        
        payload = {
            "sender": AGENT_NAME,
            "role": ROLE,
            "content": content
        }
        
        response = httpx.post(url, json=payload)
        response.raise_for_status()
        
        result = response.json()
        logger.info(f"Message sent successfully with ID: {result.get('message_id')}")
        return True
    
    except Exception as e:
        logger.error(f"Error sending message: {e}")
        return False


def main():
    """Main loop for the agent."""
    logger.info(f"Starting PRO agent '{AGENT_NAME}' for debate {DEBATE_ID}")
    logger.info(f"Using model: {MODEL}")
    logger.info(f"MCP server: {MCP_SERVER_URL}")
    
    while True:
        try:
            # Check if it's our turn
            if check_turn():
                # Get current context
                messages = get_context()
                
                if not messages:
                    logger.warning("No messages in context, skipping turn")
                    time.sleep(POLL_INTERVAL)
                    continue
                
                # Build prompt from context
                prompt = build_prompt(messages)
                logger.debug(f"Generated prompt: {prompt}")
                
                # Generate response
                raw_response = generate_response(prompt)
                logger.debug(f"Raw response: {raw_response}")
                
                # Parse and clean response
                final_response = parse_response(raw_response)
                logger.info(f"Final response: {final_response}")
                
                # Send the message
                success = send_message(final_response)
                
                if success:
                    logger.info("Turn completed successfully")
                else:
                    logger.error("Failed to complete turn")
            
            # Sleep before next check
            time.sleep(POLL_INTERVAL)
            
        except KeyboardInterrupt:
            logger.info("Agent stopped by user")
            break
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    main() 