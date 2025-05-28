#!/usr/bin/env python3
"""
Agent Launcher for Debate Day 2.0

This script simplifies launching one or all debate agents for an existing debate.
Use this when you need to launch agents separately or restart a specific agent.
"""

import os
import sys
import time
import argparse
import subprocess
from pathlib import Path
from typing import List, Optional, Dict

# Add the parent directory to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Launch one or all debate agents for an existing debate"
    )
    
    # Required arguments
    parser.add_argument(
        "--debate-id", 
        "--debate_id",
        type=str, 
        required=True,
        dest="debate_id",
        help="ID of the existing debate"
    )
    
    # Optional arguments
    parser.add_argument(
        "--role",
        type=str,
        choices=["pro", "con", "mod", "all"],
        default="all",
        help="Agent role to launch (pro, con, mod, or all) (default: all)"
    )
    
    parser.add_argument(
        "--model", 
        type=str, 
        default="llama3",
        help="Model to use for the agent(s) (default: llama3)"
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
    
    parser.add_argument(
        "--pro-name", 
        "--pro_name",
        type=str, 
        default="Alex",
        dest="pro_name",
        help="Name for the Pro agent (default: Alex)"
    )
    
    parser.add_argument(
        "--con-name", 
        "--con_name",
        type=str, 
        default="Ben",
        dest="con_name",
        help="Name for the Con agent (default: Ben)"
    )
    
    parser.add_argument(
        "--mod-name", 
        "--mod_name",
        type=str, 
        default="Mia",
        dest="mod_name",
        help="Name for the Moderator agent (default: Mia)"
    )
    
    parser.add_argument(
        "--debug", 
        action="store_true",
        help="Enable debug mode with more verbose output"
    )
    
    parser.add_argument(
        "--no-checks", 
        action="store_true",
        help="Skip pre-launch checks (MCP server and Ollama)"
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


def check_agent_code(role: str, agent_dir: str, debug: bool = False) -> bool:
    """
    Check if the agent code exists and has the required files.
    
    Args:
        role: Agent role ("pro", "con", or "mod")
        agent_dir: Base directory for agents
        debug: Whether to print debug information
        
    Returns:
        True if the agent code exists, False otherwise
    """
    agent_path = Path(agent_dir) / role
    main_path = agent_path / "main.py"
    
    if not agent_path.exists():
        print(f"Error: Agent directory not found: {agent_path}")
        return False
        
    if not main_path.exists():
        print(f"Error: Agent main.py not found: {main_path}")
        return False
    
    # Check for other required files
    required_files = ["strategy.py", "llm_config.py"]
    missing_files = [f for f in required_files if not (agent_path / f).exists()]
    
    if missing_files:
        print(f"Warning: Missing agent files: {', '.join(missing_files)}")
        print(f"This may cause the agent to fail.")
    
    if debug:
        print(f"Debug: Agent files for {role}:")
        for f in agent_path.glob("*.py"):
            print(f"  - {f.name}")
    
    return True


def check_mcp_server(mcp_url: str, debug: bool = False) -> bool:
    """
    Check if the MCP server is running.
    
    Args:
        mcp_url: URL of the MCP server
        debug: Whether to print debug information
        
    Returns:
        True if the server is running, False otherwise
    """
    try:
        import httpx
        
        if debug:
            print(f"Debug: Testing connection to MCP server at {mcp_url}")
        
        # Try to access the API docs endpoint which should always exist
        response = httpx.get(f"{mcp_url}/docs", timeout=5.0)
        
        # We don't use raise_for_status() here because we're just checking if the server responds
        if response.status_code < 500:  # Any response below 500 means server is up
            if debug:
                print(f"Debug: MCP server responded with status {response.status_code}")
            return True
        else:
            print(f"Error: MCP server responded with error {response.status_code}")
            return False
    except Exception as e:
        print(f"Error: Could not connect to MCP server at {mcp_url}")
        print(f"Error details: {e}")
        print("Make sure the MCP server is running and accessible.")
        return False


def check_ollama(debug: bool = False) -> bool:
    """
    Check if Ollama is running.
    
    Args:
        debug: Whether to print debug information
        
    Returns:
        True if Ollama is running, False otherwise
    """
    try:
        import httpx
        
        if debug:
            print("Debug: Testing connection to Ollama at http://localhost:11434")
        
        response = httpx.get("http://localhost:11434/api/tags", timeout=5.0)
        response.raise_for_status()
        
        if debug:
            models = response.json().get("models", [])
            model_names = [m.get("name") for m in models]
            print(f"Debug: Ollama is running with models: {', '.join(model_names)}")
        
        return True
    except Exception as e:
        print("Error: Could not connect to Ollama at http://localhost:11434")
        print(f"Error details: {e}")
        print("Make sure Ollama is running with the required models.")
        return False


def launch_agent(role: str, agent_dir: str, debug: bool = False) -> Optional[subprocess.Popen]:
    """
    Launch an agent as a subprocess.
    
    Args:
        role: Agent role ("pro", "con", or "mod")
        agent_dir: Base directory for agents
        debug: Whether to run in debug mode
        
    Returns:
        Subprocess handle or None if failed
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
        
        # Run the agent with the python interpreter
        cmd = [sys.executable, str(agent_path)]
        
        if debug:
            print(f"Debug: Running command: {' '.join(cmd)}")
            print(f"Debug: Working directory: {os.getcwd()}")
            
            # Run with normal output in debug mode
            process = subprocess.Popen(
                cmd,
                env=os.environ.copy(),  # Pass current environment
                text=True
            )
        else:
            # Capture output in normal mode
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                env=os.environ.copy()  # Pass current environment
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
    
    # In debug mode, show all arguments
    if args.debug:
        print("Debug: Command-line arguments:")
        for arg, value in vars(args).items():
            print(f"  {arg}: {value}")
    
    # Pre-launch checks unless --no-checks is specified
    if not args.no_checks:
        if not check_mcp_server(args.mcp_url, args.debug):
            print("Error: MCP server check failed.")
            user_continue = input("Do you want to continue anyway? (y/n): ")
            if user_continue.lower() != 'y':
                print("Exiting.")
                sys.exit(1)
        
        if not check_ollama(args.debug):
            print("Warning: Ollama check failed. Agents may not function properly.")
            user_continue = input("Do you want to continue anyway? (y/n): ")
            if user_continue.lower() != 'y':
                print("Exiting.")
                sys.exit(1)
    elif args.debug:
        print("Debug: Skipping pre-launch checks (--no-checks specified)")
    
    # Determine which roles to launch
    roles_to_launch = []
    if args.role == "all":
        roles_to_launch = ["pro", "con", "mod"]
    else:
        roles_to_launch = [args.role]
    
    # Map roles to agent names
    agent_configs = {
        "pro": args.pro_name,
        "con": args.con_name,
        "mod": args.mod_name
    }
    
    # Check agent code before launching
    for role in roles_to_launch:
        if not check_agent_code(role, args.agent_dir, args.debug):
            print(f"Error: Code check for {role} agent failed. Skipping.")
            roles_to_launch.remove(role)
    
    if not roles_to_launch:
        print("Error: No agents to launch. Exiting.")
        sys.exit(1)
    
    # Create .env files and launch agents
    processes = []
    for role in roles_to_launch:
        # Create/update .env file
        create_env_file(
            role=role,
            debate_id=args.debate_id,
            agent_name=agent_configs[role],
            model=args.model,
            mcp_url=args.mcp_url,
            agent_dir=args.agent_dir
        )
        
        # Launch the agent
        process = launch_agent(role=role, agent_dir=args.agent_dir, debug=args.debug)
        if process:
            processes.append((role, process))
    
    if not processes:
        print("No agents were launched. Check for errors above.")
        return
    
    print(f"\n{len(processes)} agent(s) launched! Press Ctrl+C to terminate.")
    
    try:
        # Monitor the processes and print their output
        while processes:
            for role, process in processes[:]:
                # Check if the process has terminated
                if process.poll() is not None:
                    print(f"{role.upper()} agent (PID {process.pid}) terminated with code {process.returncode}")
                    processes.remove((role, process))
                    continue
                
                # Skip output reading in debug mode since it's directly printed to console
                if args.debug:
                    continue
                
                # Read and print output
                if process.stdout:
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


if __name__ == "__main__":
    main() 