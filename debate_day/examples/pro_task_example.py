"""
Example demonstrating how to use the pro_task function with the DebateController.
"""

import sys
import os
from typing import Dict, Any
import json
from datetime import datetime

# Add the parent directory to sys.path to allow importing debate_day modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from controller import DebateController, AgentTurn
from protocol import DebateProtocol, DebateContext
from tasks.pro_task import pro_task

def demonstrate_pro_task():
    """Demonstrate how to use the pro_task function with the DebateController."""
    print("=== Pro Task Example ===")
    
    # Create a new debate controller
    topic = "Should artificial intelligence be regulated by governments?"
    max_rounds = 2
    controller = DebateController(topic=topic, max_rounds=max_rounds)
    
    print(f"Topic: {topic}")
    print(f"Maximum rounds: {max_rounds}")
    print()
    
    # Get initial messages (just the topic at this point)
    initial_messages = controller.get_all_messages()
    print(f"Initial messages: {len(initial_messages)}")
    
    # Generate Ava's initial argument using pro_task
    print("Generating initial Pro argument...")
    pro_message = pro_task(initial_messages)
    print(f"Pro message: {pro_message['content']}")
    
    # Add to controller
    controller.add_message(pro_message)
    print(f"Messages after Pro argument: {len(controller.get_all_messages())}")
    print()
    
    # Simulate Con's response
    print("Simulating Con's response...")
    con_message = DebateProtocol.argument_message(
        content="Government regulation would stifle innovation and create bureaucratic obstacles to progress.",
        side="con",
        agent_id="ben",
        round_number=0
    )
    controller.add_message(con_message)
    print(f"Con message: {con_message['content']}")
    print(f"Messages after Con argument: {len(controller.get_all_messages())}")
    print()
    
    # Get Ava's rebuttal using pro_task
    print("Generating Pro rebuttal...")
    recent_messages = controller.get_all_messages()
    pro_rebuttal = pro_task(recent_messages)
    
    # Add to controller
    controller.add_message(pro_rebuttal)
    print(f"Pro rebuttal: {pro_rebuttal['content']}")
    print(f"Round: {pro_rebuttal['round']}")
    print()
    
    # Show all messages in the debate so far
    print("=== Complete Debate So Far ===")
    for i, msg in enumerate(controller.get_all_messages()):
        print(f"Message {i+1}:")
        print(f"  Type: {msg['type']}")
        print(f"  Content: {msg['content']}")
        if "agent_id" in msg:
            print(f"  Agent: {msg['agent_id']}")
        if "round" in msg:
            print(f"  Round: {msg['round']}")
        print()
    
    # Export the debate to a file
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'outputs')
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"pro_task_example_{timestamp}.json"
    output_path = os.path.join(output_dir, filename)
    
    with open(output_path, 'w') as f:
        json.dump(controller.to_dict(), f, indent=2)
    
    print(f"Debate saved to: {output_path}")
    print("Example complete!")

if __name__ == "__main__":
    demonstrate_pro_task() 