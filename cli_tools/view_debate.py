#!/usr/bin/env python3
"""
Debate Viewer for Debate Day 2.0

This script allows you to watch a debate in progress by polling the MCP server
and displaying messages as they are added.
"""

import os
import sys
import time
import argparse
import httpx
from typing import Dict, List, Any, Optional
from pathlib import Path
from datetime import datetime

# Add the parent directory to sys.path so we can import from debate_day
sys.path.insert(0, str(Path(__file__).parent.parent))

from debate_day.protocol import Role


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="View a debate in progress"
    )
    
    # Required arguments
    parser.add_argument(
        "--debate-id", 
        "--debate_id",  # Allow both formats
        type=str, 
        required=True,
        dest="debate_id",
        help="ID of the debate to view"
    )
    
    # Optional arguments
    parser.add_argument(
        "--mcp-url", 
        type=str, 
        default="http://localhost:8000",
        help="URL of the MCP server (default: http://localhost:8000)"
    )
    
    parser.add_argument(
        "--refresh", 
        type=float, 
        default=2.0,
        help="Refresh interval in seconds (default: 2.0)"
    )
    
    parser.add_argument(
        "--clear", 
        action="store_true",
        help="Clear the terminal between refreshes"
    )
    
    return parser.parse_args()


def get_debate_info(debate_id: str, mcp_url: str) -> Optional[Dict[str, Any]]:
    """
    Get information about a debate.
    
    Args:
        debate_id: ID of the debate
        mcp_url: URL of the MCP server
        
    Returns:
        Debate information or None if not found
    """
    try:
        url = f"{mcp_url}/api/debate/{debate_id}"
        response = httpx.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error retrieving debate info: {e}")
        return None


def format_messages(messages: List[Dict[str, Any]]) -> str:
    """
    Format a list of messages for display.
    
    Args:
        messages: List of message dictionaries
        
    Returns:
        Formatted message text
    """
    if not messages:
        return "No messages yet."
    
    formatted = []
    
    # Group messages by round
    messages_by_round = {}
    for msg in messages:
        round_num = msg["round"]
        if round_num not in messages_by_round:
            messages_by_round[round_num] = []
        messages_by_round[round_num].append(msg)
    
    # Format each round
    for round_num in sorted(messages_by_round.keys()):
        if round_num > 0:
            formatted.append(f"\n--- ROUND {round_num} ---\n")
        
        # Format messages in this round
        for msg in messages_by_round[round_num]:
            timestamp = datetime.fromisoformat(msg["timestamp"].replace("Z", "+00:00"))
            time_str = timestamp.strftime("%H:%M:%S")
            
            if msg["role"] == "pro":
                role_display = "PRO (Alex)"
                prefix = "\033[32m"  # Green
            elif msg["role"] == "con":
                role_display = "CON (Ben)"
                prefix = "\033[31m"  # Red
            elif msg["role"] == "mod":
                role_display = "MODERATOR (Mia)"
                prefix = "\033[33m"  # Yellow
            else:
                role_display = "SYSTEM"
                prefix = "\033[36m"  # Cyan
            
            # Format the message with color
            formatted.append(f"{prefix}[{time_str}] {role_display}:\033[0m {msg['content']}")
    
    return "\n\n".join(formatted)


def display_debate_status(debate: Dict[str, Any], clear: bool = False):
    """
    Display the current status of a debate.
    
    Args:
        debate: Debate information dictionary
        clear: Whether to clear the terminal before displaying
    """
    if clear:
        os.system('cls' if os.name == 'nt' else 'clear')
    
    # Extract info
    debate_info = debate["debate"]
    messages = debate["messages"]
    turn_info = debate["current_turn"]
    
    # Format and print header
    print("\033[1m" + "=" * 80 + "\033[0m")
    print(f"\033[1mDEBATE: {debate_info['topic']}\033[0m")
    print(f"ID: {debate_info['debate_id']} | Status: {debate_info['status']} | Rounds: {debate_info['num_rounds']}")
    
    # Print turn information if available
    if turn_info:
        next_speaker = turn_info["next_speaker"]
        if next_speaker == "pro":
            speaker_display = "\033[32mPRO (Alex)\033[0m"
        elif next_speaker == "con":
            speaker_display = "\033[31mCON (Ben)\033[0m"
        elif next_speaker == "mod":
            speaker_display = "\033[33mMODERATOR (Mia)\033[0m"
        else:
            speaker_display = next_speaker
            
        print(f"Current Round: {turn_info['current_round']} | Next Speaker: {speaker_display}")
    
    if debate_info["winner"]:
        winner = debate_info["winner"]
        if winner == "pro":
            winner_display = "\033[32mPRO (Alex)\033[0m"
        elif winner == "con":
            winner_display = "\033[31mCON (Ben)\033[0m"
        else:
            winner_display = winner
        print(f"Winner: {winner_display}")
    
    print("\033[1m" + "=" * 80 + "\033[0m")
    
    # Print messages
    print("\n" + format_messages(messages) + "\n")
    
    print("\033[1m" + "=" * 80 + "\033[0m")


def main():
    """Main entry point."""
    args = parse_arguments()
    
    print(f"Viewing debate {args.debate_id}...")
    print(f"Press Ctrl+C to exit")
    
    last_message_count = 0
    
    try:
        while True:
            # Get debate information
            debate = get_debate_info(args.debate_id, args.mcp_url)
            
            if debate:
                current_message_count = len(debate["messages"])
                
                # Only refresh display if there are new messages or first time
                if current_message_count > last_message_count or last_message_count == 0:
                    display_debate_status(debate, args.clear)
                    last_message_count = current_message_count
                
                # If debate is finished, show final result and exit
                if debate["debate"]["status"] == "finished":
                    print("\nDebate has concluded!")
                    if debate["debate"]["winner"]:
                        winner = debate["debate"]["winner"]
                        if winner == "pro":
                            print("\033[32mPRO side (Alex) has won the debate!\033[0m")
                        elif winner == "con":
                            print("\033[31mCON side (Ben) has won the debate!\033[0m")
                        else:
                            print(f"{winner} has won the debate!")
                    else:
                        print("No winner was declared.")
                    break
            
            # Wait before checking again
            time.sleep(args.refresh)
            
    except KeyboardInterrupt:
        print("\nExiting debate viewer...")


if __name__ == "__main__":
    main() 