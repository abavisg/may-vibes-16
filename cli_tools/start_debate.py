#!/usr/bin/env python3
"""
Debate Bootstrapper for Debate Day 2.0

This script initializes a new debate via the MCP server and optionally
launches the pro, con, and moderator agents as subprocesses.
"""

import os
import sys
import time
import argparse
import subprocess
import uuid
from datetime import datetime
from pathlib import Path
import httpx
from typing import Dict, Optional, List, Any

# Add the parent directory to sys.path so we can import from debate_day
sys.path.insert(0, str(Path(__file__).parent.parent))

from debate_day.protocol import generate_debate_id


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Start a new debate and optionally launch agent processes"
    )
    
    # Required arguments
    parser.add_argument(
        "--topic", 
        type=str, 
        required=True,
        help="The debate topic/resolution"
    )
    
    # Optional arguments
    parser.add_argument(
        "--rounds", 
        type=int, 
        default=1,
        help="Number of debate rounds (default: 1)"
    )
    
    parser.add_argument(
        "--debate-id", 
        "--debate_id",  # Allow both formats
        type=str, 
        default=None,
        dest="debate_id",
        help="Custom debate ID (auto-generated if not provided)"
    )
    
    parser.add_argument(
        "--launch-agents", 
        action="store_true",
        help="Launch pro, con, and mod agents as subprocesses"
    )
    
    parser.add_argument(
        "--model", 
        type=str, 
        default="llama3",
        help="Model to use for all agents (default: llama3)"
    )
    
    parser.add_argument(
        "--mcp-url", 
        type=str, 
        default="http://localhost:8000",
        help="URL of the MCP server (default: http://localhost:8000)"
    )
    
    parser.add_argument(
        "--agent-dir", 
        type=str, 
        default="debate_day/agents",
        help="Directory containing agent code (default: debate_day/agents)"
    )
    
    # Agent name parameters
    parser.add_argument(
        "--pro-name", 
        "--pro_name",  # Allow both formats
        type=str, 
        default="Alex",
        dest="pro_name",
        help="Name for the Pro agent (default: Alex)"
    )
    
    parser.add_argument(
        "--con-name", 
        "--con_name",  # Allow both formats
        type=str, 
        default="Ben",
        dest="con_name",
        help="Name for the Con agent (default: Ben)"
    )
    
    parser.add_argument(
        "--mod-name", 
        "--mod_name",  # Allow both formats
        type=str, 
        default="Mia",
        dest="mod_name",
        help="Name for the Moderator agent (default: Mia)"
    )
    
    return parser.parse_args()


def create_env_file(
    role: str, 
    debate_id: str, 
    agent_name: str,
    model: str,
    mcp_url: str,
    agent_dir: str
) -> None:
    """
    Create/overwrite .env file for an agent.
    
    Args:
        role: Agent role ("pro", "con", or "mod")
        debate_id: ID of the debate
        agent_name: Name of the agent
        model: Model to use
        mcp_url: URL of the MCP server
        agent_dir: Base directory for agents
    """
    # Create the .env file content
    env_content = f"""# {role.upper()} Agent Configuration
ROLE={role}
MODEL={model}
MCP_SERVER_URL={mcp_url}
AGENT_NAME={agent_name}
DEBATE_ID={debate_id}
"""
    
    # Determine path for the .env file
    env_path = Path(agent_dir) / role / ".env"
    
    # Create directory if it doesn't exist
    env_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Write the .env file
    with open(env_path, "w") as f:
        f.write(env_content)
    
    print(f"Created .env file for {role} agent at {env_path}")


def start_debate(
    topic: str, 
    rounds: int, 
    debate_id: Optional[str] = None, 
    mcp_url: str = "http://localhost:8000"
) -> str:
    """
    Start a new debate via the MCP server.
    
    Args:
        topic: The debate topic/resolution
        rounds: Number of debate rounds
        debate_id: Optional custom debate ID
        mcp_url: URL of the MCP server
        
    Returns:
        The debate ID
    """
    # Generate debate ID if not provided
    if not debate_id:
        debate_id = generate_debate_id()
    
    # Build the request payload
    payload = {
        "topic": topic,
        "rounds": rounds,
        "debate_id": debate_id
    }
    
    # Send the request to the MCP server
    try:
        url = f"{mcp_url}/api/start"
        response = httpx.post(url, json=payload)
        response.raise_for_status()
        
        result = response.json()
        print(f"Debate started successfully!")
        print(f"Debate ID: {debate_id}")
        print(f"Topic: {topic}")
        print(f"Rounds: {rounds}")
        
        return debate_id
    
    except Exception as e:
        print(f"Error starting debate: {e}")
        sys.exit(1)


def launch_agent(role: str, agent_dir: str) -> subprocess.Popen:
    """
    Launch an agent as a subprocess.
    
    Args:
        role: Agent role ("pro", "con", or "mod")
        agent_dir: Base directory for agents
        
    Returns:
        Subprocess handle
    """
    # Determine the path to the agent's main.py
    agent_path = Path(agent_dir) / role / "main.py"
    
    # Make sure the script is executable
    if os.name != "nt":  # Skip on Windows
        try:
            agent_path.chmod(agent_path.stat().st_mode | 0o111)
        except Exception as e:
            print(f"Warning: Could not make {agent_path} executable: {e}")
    
    # Launch the agent
    try:
        print(f"Launching {role} agent...")
        
        # Use python explicitly for better cross-platform compatibility
        process = subprocess.Popen(
            [sys.executable, str(agent_path)],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        
        print(f"{role.upper()} agent started with PID {process.pid}")
        return process
    
    except Exception as e:
        print(f"Error launching {role} agent: {e}")
        return None


def main():
    """Main entry point."""
    # Parse command-line arguments
    args = parse_arguments()
    
    # Start the debate
    debate_id = start_debate(
        topic=args.topic,
        rounds=args.rounds,
        debate_id=args.debate_id,
        mcp_url=args.mcp_url
    )
    
    # If --launch-agents is passed, set up and launch the agents
    if args.launch_agents:
        # Create .env files for each agent with their custom names
        agent_configs = {
            "pro": args.pro_name,
            "con": args.con_name,
            "mod": args.mod_name
        }
        
        for role, name in agent_configs.items():
            create_env_file(
                role=role,
                debate_id=debate_id,
                agent_name=name,
                model=args.model,
                mcp_url=args.mcp_url,
                agent_dir=args.agent_dir
            )
        
        # Launch agents
        processes = []
        for role in agent_configs.keys():
            process = launch_agent(role=role, agent_dir=args.agent_dir)
            if process:
                processes.append((role, process))
        
        print("\nAll agents launched! Press Ctrl+C to terminate.")
        
        try:
            # Monitor the processes and print their output
            while processes:
                for role, process in processes[:]:
                    # Check if the process has terminated
                    if process.poll() is not None:
                        print(f"{role.upper()} agent (PID {process.pid}) terminated with code {process.returncode}")
                        processes.remove((role, process))
                        continue
                    
                    # Read and print output
                    output = process.stdout.readline()
                    if output:
                        print(f"[{role.upper()}] {output.strip()}")
                
                # Sleep to avoid high CPU usage
                time.sleep(0.1)
            
            print("All agents have completed.")
        
        except KeyboardInterrupt:
            print("\nTerminating agents...")
            for role, process in processes:
                try:
                    process.terminate()
                    print(f"Terminated {role.upper()} agent (PID {process.pid})")
                except Exception as e:
                    print(f"Error terminating {role.upper()} agent: {e}")
    
    else:
        print("\nAgents were not launched. To start agents separately:")
        print(f"  1. Set DEBATE_ID={debate_id} in each agent's .env file")
        print(f"  2. Run each agent's main.py script")
        

if __name__ == "__main__":
    main() 