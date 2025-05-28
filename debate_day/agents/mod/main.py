#!/usr/bin/env python3
"""
Moderator Agent for Debate Day 2.0.

This agent participates in debates as the MODERATOR, using the MCP server
for communication and coordination, and provides final verdicts.
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
from debate_day.agents.mod.strategy import build_prompt, parse_response
from debate_day.agents.mod.llm_config import generate_response

# Create logs directory at project root
project_root = Path(__file__).parent.parent.parent.parent # This assumes agents/mod/main.py, so ../../../ is root
logs_dir = project_root / "logs"
logs_dir.mkdir(parents=True, exist_ok=True)

# Configure logging
logger.remove()
logger.add(
    logs_dir / "mod_agent_{time}.log", # Updated path
    rotation="10 MB",
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
)
logger.add(lambda msg: print(msg), level="INFO", format="{message}")

# Load environment variables
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

# Configuration
ROLE = os.getenv("ROLE", "mod")
MODEL = os.getenv("MODEL", "llama3")
MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "http://localhost:8000")
AGENT_NAME = os.getenv("AGENT_NAME", "Mia")
DEBATE_ID = os.getenv("DEBATE_ID", "test-debate-id-001")

# Polling interval (seconds)
POLL_INTERVAL = 10


def check_turn() -> Dict[str, Any]:
    """
    Check if it's this agent's turn and the debate status.
    
    Returns:
        A dictionary with 'is_our_turn' (bool) and 'debate_status' (str).
    """
    try:
        logger.info(f"Checking turn and status for {ROLE}...")
        url = f"{MCP_SERVER_URL}/api/turn/{DEBATE_ID}"
        response = httpx.get(url)
        response.raise_for_status()
        
        data = response.json()
        is_our_turn = data.get("next_speaker") == ROLE
        debate_status = data.get("status", "unknown")
        
        if is_our_turn:
            logger.info(f"It's {ROLE}'s turn in round {data.get('current_round')}! Debate status: {debate_status}")
        else:
            logger.debug(f"Not our turn. Current speaker: {data.get('next_speaker')}. Debate status: {debate_status}")
            
        return {"is_our_turn": is_our_turn, "debate_status": debate_status}
    
    except Exception as e:
        logger.error(f"Error checking turn: {e}")
        return {"is_our_turn": False, "debate_status": "error"}


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


def extract_winner(response: str) -> str:
    """
    Extract the winner from the response.
    
    Args:
        response: The moderator's verdict
        
    Returns:
        The winner's role ("pro" or "con") or None if not found
    """
    response_lower = response.lower()
    
    # Try to find explicit winner declarations
    if "pro wins" in response_lower or "declare pro" in response_lower or "winner is pro" in response_lower:
        return "pro"
    elif "con wins" in response_lower or "declare con" in response_lower or "winner is con" in response_lower:
        return "con"
    
    # Check for more subtle indications
    pro_score = 0
    con_score = 0
    
    pro_indicators = ["pro made the stronger case", "pro side was more persuasive", "pro had better arguments"]
    con_indicators = ["con made the stronger case", "con side was more persuasive", "con had better arguments"]
    
    for indicator in pro_indicators:
        if indicator in response_lower:
            pro_score += 1
            
    for indicator in con_indicators:
        if indicator in response_lower:
            con_score += 1
    
    if pro_score > con_score:
        return "pro"
    elif con_score > pro_score:
        return "con"
    
    # Default to first side mentioned if scoring is tied
    if "pro" in response_lower and "con" in response_lower:
        pro_pos = response_lower.find("pro")
        con_pos = response_lower.find("con")
        return "pro" if pro_pos < con_pos else "con"
    
    # No clear winner found
    return None


def send_message(content: str) -> bool:
    """
    Send a message to the debate.
    
    Args:
        content: The message content
        
    Returns:
        True if successful, False otherwise
    """
    try:
        logger.info("Sending verdict...")
        url = f"{MCP_SERVER_URL}/api/message/{DEBATE_ID}"
        
        # Extract the winner from the content
        winner = extract_winner(content)
        logger.info(f"Extracted winner from verdict: {winner}")
        
        # Prepare metadata with winner if found
        metadata = {"winner": winner} if winner else {}
        
        payload = {
            "sender": AGENT_NAME,
            "role": ROLE,
            "content": content,
            "metadata": metadata
        }
        
        response = httpx.post(url, json=payload)
        response.raise_for_status()
        
        result = response.json()
        logger.info(f"Verdict sent successfully with ID: {result.get('message_id')}")
        return True
    
    except Exception as e:
        logger.error(f"Error sending verdict: {e}")
        return False


def main():
    """Main loop for the agent."""
    logger.info(f"Starting MODERATOR agent '{AGENT_NAME}' for debate {DEBATE_ID}")
    logger.info(f"Using model: {MODEL}")
    logger.info(f"MCP server: {MCP_SERVER_URL}")
    
    while True:
        try:
            turn_info = check_turn()
            
            if turn_info["debate_status"] == "finished" or turn_info["debate_status"] == "error":
                # Moderator might have already spoken if status is finished, or an error occurred.
                logger.info(f"Debate status is '{turn_info["debate_status"]}'. MODERATOR agent '{AGENT_NAME}' stopping.")
                break
            
            if turn_info["is_our_turn"]:
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
                logger.info(f"Final verdict: {final_response}")
                
                # Send the message
                success = send_message(final_response)
                
                if success:
                    logger.info("Verdict delivered successfully")
                else:
                    logger.error("Failed to deliver verdict")
                
                # As the moderator, our job is done after delivering the verdict
                logger.info("Moderator's job is complete, exiting")
                break
            
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