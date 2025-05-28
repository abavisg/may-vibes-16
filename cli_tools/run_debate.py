#!/usr/bin/env python3
"""
Debate Day All-in-One Runner

This script provides a simple way to run a complete debate in one step:
1. Starts the MCP server
2. Creates a new debate
3. Launches all agent processes
4. Shows debate progress in a dedicated viewer

Use this script for the simplest possible setup to run a debate.
"""

import os
import sys
import time
import argparse
import subprocess
import signal
import uuid
from pathlib import Path
import threading
from typing import List, Dict, Optional

# Add the parent directory to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Global variables to track processes
mcp_process = None
agent_processes = []
viewer_process = None
running = True


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Run a complete debate in one step (MCP server + debate + agents)"
    )
    
    # Debate configuration
    parser.add_argument(
        "--topic", 
        type=str, 
        default="Is artificial intelligence beneficial for humanity?",
        help="The debate topic/resolution (default: AI benefit topic)"
    )
    
    parser.add_argument(
        "--rounds", 
        type=int, 
        default=1,
        help="Number of debate rounds (default: 1)"
    )
    
    parser.add_argument(
        "--debate-id", 
        "--debate_id",
        type=str, 
        default=None,
        dest="debate_id",
        help="Custom debate ID (auto-generated if not provided)"
    )
    
    # Agent configuration
    parser.add_argument(
        "--model", 
        type=str, 
        default="llama3",
        help="Model to use for all agents (default: llama3)"
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
    
    # Server configuration
    parser.add_argument(
        "--port", 
        type=int, 
        default=8000,
        help="Port for the MCP server (default: 8000)"
    )
    
    parser.add_argument(
        "--host", 
        type=str, 
        default="localhost",
        help="Host for the MCP server (default: localhost)"
    )
    
    parser.add_argument(
        "--wait", 
        type=int, 
        default=5,
        help="Seconds to wait for MCP server to start (default: 5)"
    )
    
    # Viewer options
    parser.add_argument(
        "--no-viewer",
        action="store_true",
        help="Disable the debate viewer"
    )
    
    parser.add_argument(
        "--clear-viewer",
        action="store_true",
        help="Clear the terminal between viewer updates"
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


def start_mcp_server(host: str, port: int) -> subprocess.Popen:
    """
    Start the MCP server as a subprocess.
    
    Args:
        host: Host to bind the server to
        port: Port to bind the server to
        
    Returns:
        Subprocess handle
    """
    print(f"Starting MCP server on {host}:{port}...")
    
    # Path to the MCP server script
    server_path = "debate_day/run_mcp_server.py"
    
    # Environment variables for the server
    env = os.environ.copy()
    env["HOST"] = host
    env["PORT"] = str(port)
    
    # Start the server
    process = subprocess.Popen(
        [sys.executable, server_path],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )
    
    print(f"MCP server started with PID {process.pid}")
    return process


def monitor_server_output(process: subprocess.Popen):
    """
    Monitor the output of the MCP server.
    
    Args:
        process: Subprocess handle
    """
    global running
    
    while running and process.poll() is None:
        if process.stdout:
            line = process.stdout.readline()
            if line:
                print(f"[MCP] {line.strip()}")
        else:
            time.sleep(0.1)


def wait_for_server(host: str, port: int, timeout: int = 5) -> bool:
    """
    Wait for the MCP server to start.
    
    Args:
        host: Server host
        port: Server port
        timeout: Timeout in seconds
        
    Returns:
        True if the server started, False otherwise
    """
    import socket
    import time
    
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            # Try to connect to the server
            with socket.create_connection((host, port), timeout=1):
                print(f"MCP server is running on {host}:{port}")
                return True
        except (socket.timeout, ConnectionRefusedError):
            # Wait a bit and try again
            time.sleep(0.5)
            print("Waiting for MCP server to start...")
    
    print(f"Timed out waiting for MCP server to start on {host}:{port}")
    return False


def create_debate(
    topic: str, 
    rounds: int, 
    debate_id: Optional[str] = None, 
    host: str = "localhost",
    port: int = 8000
) -> str:
    """
    Create a new debate via the MCP server.
    
    Args:
        topic: The debate topic/resolution
        rounds: Number of debate rounds
        debate_id: Optional custom debate ID
        host: Server host
        port: Server port
        
    Returns:
        The debate ID
    """
    import httpx
    
    # Generate debate ID if not provided
    if not debate_id:
        debate_id = str(uuid.uuid4())
    
    # Build the request payload
    payload = {
        "topic": topic,
        "rounds": rounds,
        "debate_id": debate_id
    }
    
    # Send the request to the MCP server
    try:
        url = f"http://{host}:{port}/api/start"
        response = httpx.post(url, json=payload, timeout=10.0)
        response.raise_for_status()
        
        result = response.json()
        print(f"Debate created successfully!")
        print(f"Debate ID: {debate_id}")
        print(f"Topic: {topic}")
        print(f"Rounds: {rounds}")
        
        return debate_id
    
    except Exception as e:
        print(f"Error creating debate: {e}")
        sys.exit(1)


def launch_agent(
    role: str, 
    agent_dir: str, 
    debate_id: str,
    agent_name: str,
    model: str,
    mcp_url: str
) -> subprocess.Popen:
    """
    Launch an agent as a subprocess.
    
    Args:
        role: Agent role ("pro", "con", or "mod")
        agent_dir: Base directory for agents
        debate_id: Debate ID
        agent_name: Agent name
        model: Model to use
        mcp_url: MCP server URL
        
    Returns:
        Subprocess handle
    """
    # Create the .env file
    create_env_file(
        role=role,
        debate_id=debate_id,
        agent_name=agent_name,
        model=model,
        mcp_url=mcp_url,
        agent_dir=agent_dir
    )
    
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
        
        # Run the agent
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


def monitor_agent_output(role: str, process: subprocess.Popen):
    """
    Monitor the output of an agent.
    
    Args:
        role: Agent role
        process: Subprocess handle
    """
    global running
    
    while running and process.poll() is None:
        if process.stdout:
            line = process.stdout.readline()
            if line:
                print(f"[{role.upper()}] {line.strip()}")
        else:
            time.sleep(0.1)


def launch_debate_viewer(debate_id: str, mcp_url: str, clear: bool = False) -> subprocess.Popen:
    """
    Launch the debate viewer as a subprocess.
    
    Args:
        debate_id: Debate ID to view
        mcp_url: MCP server URL
        clear: Whether to clear the terminal between updates
        
    Returns:
        Subprocess handle
    """
    # Path to the viewer script
    viewer_path = Path(__file__).parent / "view_debate.py"
    
    # Build command arguments
    cmd = [sys.executable, str(viewer_path), "--debate-id", debate_id, "--mcp-url", mcp_url]
    
    if clear:
        cmd.append("--clear")
    
    # Launch the viewer
    try:
        print(f"Launching debate viewer for debate ID: {debate_id}...")
        
        # Create a new terminal window for the viewer
        if sys.platform == "darwin":  # macOS
            # Use AppleScript to open a new Terminal window
            script = f'''
            tell application "Terminal"
                do script "{' '.join(cmd)}"
                activate
            end tell
            '''
            subprocess.run(["osascript", "-e", script])
            print("Debate viewer opened in a new terminal window")
            return None
        elif sys.platform == "win32":  # Windows
            # Use start command to open a new cmd window
            process = subprocess.Popen(
                ["start", "cmd", "/k", " ".join(cmd)],
                shell=True
            )
            print("Debate viewer opened in a new command window")
            return process
        else:  # Linux and others
            # Try to use x-terminal-emulator or fall back to running in background
            try:
                cmd_str = " ".join(cmd)
                subprocess.Popen(
                    ["x-terminal-emulator", "-e", cmd_str],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                print("Debate viewer opened in a new terminal window")
                return None
            except FileNotFoundError:
                # Fall back to running in the current terminal
                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1
                )
                print(f"Debate viewer started with PID {process.pid}")
                return process
    
    except Exception as e:
        print(f"Error launching debate viewer: {e}")
        print(f"You can manually view the debate with: python {viewer_path} --debate-id {debate_id}")
        return None


def shutdown_processes():
    """Shut down all processes."""
    global mcp_process, agent_processes, viewer_process, running
    
    running = False
    print("\nShutting down processes...")
    
    # Terminate agent processes
    for role, process in agent_processes:
        try:
            if process.poll() is None:
                process.terminate()
                print(f"Terminated {role.upper()} agent (PID {process.pid})")
        except Exception as e:
            print(f"Error terminating {role.upper()} agent: {e}")
    
    # Terminate viewer process if running in current terminal
    if viewer_process and viewer_process.poll() is None:
        try:
            viewer_process.terminate()
            print(f"Terminated debate viewer (PID {viewer_process.pid})")
        except Exception as e:
            print(f"Error terminating debate viewer: {e}")
    
    # Terminate MCP server
    if mcp_process and mcp_process.poll() is None:
        try:
            mcp_process.terminate()
            print(f"Terminated MCP server (PID {mcp_process.pid})")
        except Exception as e:
            print(f"Error terminating MCP server: {e}")


def signal_handler(sig, frame):
    """Handle Ctrl+C."""
    print("\nInterrupted by user")
    shutdown_processes()
    sys.exit(0)


def main():
    """Main entry point."""
    global mcp_process, agent_processes, viewer_process
    
    # Register signal handler for Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)
    
    # Parse command-line arguments
    args = parse_arguments()
    
    try:
        # Start MCP server
        mcp_process = start_mcp_server(args.host, args.port)
        
        # Start a thread to monitor server output
        server_thread = threading.Thread(
            target=monitor_server_output,
            args=(mcp_process,),
            daemon=True
        )
        server_thread.start()
        
        # Wait for the server to start
        mcp_url = f"http://{args.host}:{args.port}"
        if not wait_for_server(args.host, args.port, args.wait):
            print("Failed to start MCP server. Exiting.")
            shutdown_processes()
            sys.exit(1)
        
        # Create a debate
        debate_id = create_debate(
            topic=args.topic,
            rounds=args.rounds,
            debate_id=args.debate_id,
            host=args.host,
            port=args.port
        )
        
        # Launch the debate viewer if not disabled
        if not args.no_viewer:
            viewer_process = launch_debate_viewer(
                debate_id=debate_id,
                mcp_url=mcp_url,
                clear=args.clear_viewer
            )
            
            # Start a thread to monitor viewer output if running in current terminal
            if viewer_process:
                viewer_thread = threading.Thread(
                    target=lambda: monitor_agent_output("VIEWER", viewer_process),
                    daemon=True
                )
                viewer_thread.start()
        
        # Launch agents
        agent_configs = {
            "pro": args.pro_name,
            "con": args.con_name,
            "mod": args.mod_name
        }
        
        # Start agents and monitoring threads
        for role, name in agent_configs.items():
            # Launch the agent
            process = launch_agent(
                role=role,
                agent_dir=args.agent_dir,
                debate_id=debate_id,
                agent_name=name,
                model=args.model,
                mcp_url=mcp_url
            )
            
            if process:
                agent_processes.append((role, process))
                
                # Start a thread to monitor agent output
                agent_thread = threading.Thread(
                    target=monitor_agent_output,
                    args=(role, process),
                    daemon=True
                )
                agent_thread.start()
        
        print(f"\nDebate started with ID: {debate_id}")
        print(f"Topic: {args.topic}")
        print(f"Rounds: {args.rounds}")
        
        if args.no_viewer:
            print("\nDebate viewer is disabled. To view the debate manually:")
            print(f"python cli_tools/view_debate.py --debate-id {debate_id}")
        
        print("\nPress Ctrl+C to terminate all processes")
        
        # Keep the main thread running
        while mcp_process.poll() is None:
            # Check if all agents have terminated
            if all(p.poll() is not None for _, p in agent_processes):
                print("All agents have terminated. Shutting down MCP server.")
                shutdown_processes()
                break
            
            time.sleep(0.5)
    
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        shutdown_processes()


if __name__ == "__main__":
    main() 