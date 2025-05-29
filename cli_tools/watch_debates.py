#!/usr/bin/env python3
"""
Debate Watcher for Debate Day 2.0

This script monitors the MCP server for new debates and automatically launches
agents when a new debate is created through the Flutter UI.
"""

import os
import sys
import time
import subprocess
import httpx
from pathlib import Path
from typing import Dict, List, Optional, Set

# Add the parent directory to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))


class DebateWatcher:
    def __init__(self, mcp_url: str = "http://localhost:8000", agent_dir: str = "debate_day/agents"):
        self.mcp_url = mcp_url
        self.agent_dir = agent_dir
        self.active_debates: Set[str] = set()
        self.running_processes: Dict[str, List[subprocess.Popen]] = {}
        
    def get_active_debates(self) -> List[Dict]:
        """Get list of active debates from the MCP server."""
        try:
            # This endpoint would need to be implemented in the MCP server
            # For now, we'll use the debate status endpoint
            response = httpx.get(f"{self.mcp_url}/api/debates", timeout=5.0)
            if response.status_code == 200:
                return response.json()
            return []
        except:
            return []
    
    def launch_agents_for_debate(self, debate_id: str) -> bool:
        """Launch agents for a specific debate."""
        print(f"\n🚀 Launching agents for debate: {debate_id}")
        
        # Use launch_agents.py to start the agents
        try:
            cmd = [
                sys.executable,
                "cli_tools/launch_agents.py",
                "--debate-id", debate_id,
                "--role", "all",
                "--pro-name", "ProAgentAlpha",
                "--con-name", "ConAgentBeta", 
                "--mod-name", "ModeratorZeta",
                "--no-checks"  # Skip checks since we're monitoring continuously
            ]
            
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True
            )
            
            # Store the process
            if debate_id not in self.running_processes:
                self.running_processes[debate_id] = []
            self.running_processes[debate_id].append(process)
            
            print(f"✅ Agents launched for debate {debate_id}")
            return True
            
        except Exception as e:
            print(f"❌ Error launching agents: {e}")
            return False
    
    def check_for_new_debates(self):
        """Check for new debates and launch agents if needed."""
        try:
            # For now, we'll monitor by trying to get debate status for recent IDs
            # In a real implementation, the MCP server would have an endpoint to list active debates
            
            # This is a simplified version - you'd need to implement proper debate discovery
            print(".", end="", flush=True)  # Progress indicator
            
        except Exception as e:
            print(f"\n⚠️ Error checking debates: {e}")
    
    def cleanup_finished_debates(self):
        """Clean up processes for finished debates."""
        for debate_id, processes in list(self.running_processes.items()):
            # Check if all processes have finished
            all_finished = all(p.poll() is not None for p in processes)
            if all_finished:
                print(f"\n🏁 All agents finished for debate {debate_id}")
                del self.running_processes[debate_id]
                self.active_debates.discard(debate_id)
    
    def run(self):
        """Main monitoring loop."""
        print("🔍 Debate Watcher Started")
        print(f"📡 Monitoring MCP server at: {self.mcp_url}")
        print("⏳ Waiting for new debates from Flutter UI...")
        print("\nPress Ctrl+C to stop\n")
        
        try:
            while True:
                self.check_for_new_debates()
                self.cleanup_finished_debates()
                time.sleep(2)  # Check every 2 seconds
                
        except KeyboardInterrupt:
            print("\n\n🛑 Stopping Debate Watcher...")
            
            # Terminate all running processes
            for debate_id, processes in self.running_processes.items():
                print(f"Terminating agents for debate {debate_id}...")
                for process in processes:
                    try:
                        process.terminate()
                    except:
                        pass
            
            print("✅ Debate Watcher stopped")


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Watch for new debates and auto-launch agents")
    parser.add_argument("--mcp-url", default="http://localhost:8000", help="MCP server URL")
    parser.add_argument("--agent-dir", default="debate_day/agents", help="Agent directory")
    
    args = parser.parse_args()
    
    watcher = DebateWatcher(mcp_url=args.mcp_url, agent_dir=args.agent_dir)
    watcher.run()


if __name__ == "__main__":
    main() 