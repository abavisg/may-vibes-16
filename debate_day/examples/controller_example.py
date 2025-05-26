"""
Example demonstrating how to use the DebateController to manage a debate.
"""

import sys
import os
from typing import Dict, Any

# Add the parent directory to sys.path to allow importing debate_day modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from controller import DebateController, AgentTurn
from protocol import DebateProtocol

def simulate_debate():
    """Simulate a debate using the DebateController."""
    print("=== DebateController Example ===")
    
    # Create a new debate controller
    topic = "Should artificial intelligence be regulated by governments?"
    max_rounds = 2
    controller = DebateController(topic=topic, max_rounds=max_rounds)
    
    print(f"Topic: {topic}")
    print(f"Maximum rounds: {max_rounds}")
    print(f"Initial state: {controller.get_debate_summary()}")
    print()
    
    # Simulate the debate flow
    while controller.turn != AgentTurn.DONE:
        current_turn = controller.turn
        current_round = controller.round_number
        
        print(f"Round {current_round}, Turn: {current_turn.value}")
        
        # Get context for the current agent
        context = controller.format_for_agent(current_turn)
        print(f"Context for {current_turn.value}:")
        print(context)
        print()
        
        # Simulate agent response
        if current_turn == AgentTurn.PRO:
            agent_id = "ava"
            side = "pro"
            if current_round == 0:
                content = "AI regulation is necessary to prevent potential harms while allowing beneficial innovation."
            else:
                content = f"Industry self-regulation has proven insufficient as evidenced by multiple ethical violations. (Round {current_round})"
        elif current_turn == AgentTurn.CON:
            agent_id = "ben"
            side = "con"
            if current_round == 0:
                content = "Government regulation would stifle innovation and create bureaucratic obstacles to progress."
            else:
                content = f"Regulatory frameworks are often outdated before implementation due to the rapid pace of AI advancement. (Round {current_round})"
        elif current_turn == AgentTurn.MOD:
            agent_id = "mia"
            side = None
            content = "After evaluating the arguments, the Pro side presented stronger evidence for balanced regulation. Winner: Ava (Pro)"
            # For moderator, use evaluation message
            message = DebateProtocol.evaluation_message(
                content=content,
                winner="pro",
                agent_id=agent_id
            )
            controller.add_message(message)
            # Advance to next agent
            controller.next_agent()
            print(f"Moderator evaluation: {content}")
            print()
            continue
        
        # Create message using DebateProtocol
        message = DebateProtocol.argument_message(
            content=content,
            side=side,
            agent_id=agent_id,
            round_number=current_round
        )
        
        # Add the message to the controller
        controller.add_message(message)
        print(f"{current_turn.value.capitalize()} response: {content}")
        print()
        
        # Advance to next agent
        next_turn, next_round = controller.next_agent()
        print(f"Next turn: {next_turn.value}, Next round: {next_round}")
        print("-" * 50)
    
    # Debate is complete
    print("\n=== Debate Complete ===")
    print(f"Final state: {controller.get_debate_summary()}")
    print()
    
    # Display all messages
    print("=== All Messages ===")
    for i, msg in enumerate(controller.get_all_messages()):
        print(f"Message {i+1}:")
        print(f"  Type: {msg['type']}")
        print(f"  Content: {msg['content']}")
        if "agent_id" in msg:
            print(f"  Agent: {msg['agent_id']}")
        if "round" in msg:
            print(f"  Round: {msg['round']}")
        print()
    
    # Save debate to dictionary and reload
    print("=== Testing Serialization ===")
    debate_dict = controller.to_dict()
    print(f"Serialized to dictionary with {len(debate_dict['messages'])} messages")
    
    # Create a new controller from the dictionary
    new_controller = DebateController.from_dict(debate_dict)
    print(f"Reloaded controller: {new_controller.get_debate_summary()}")
    print("Serialization test successful!")

if __name__ == "__main__":
    simulate_debate() 