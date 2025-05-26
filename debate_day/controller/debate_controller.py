"""
DebateController manages the flow of a debate, tracking messages, rounds, and agent transitions.

It provides methods to control the debate progression and access the message history.
"""

from typing import Dict, List, Optional, Any, Tuple
from enum import Enum
from protocol import DebateProtocol, MessageType, DebateContext

class AgentTurn(Enum):
    """Defines the possible turns in the debate sequence."""
    PRO = "pro"     # Pro agent (Ava)
    CON = "con"     # Con agent (Ben)
    MOD = "mod"     # Moderator agent (Mia)
    DONE = "done"   # Debate is complete

class DebateController:
    """
    Controls the flow of a debate, tracking messages, rounds, and agent turns.
    
    This class manages the state of a debate including:
    - The debate topic
    - The current round number
    - The current agent's turn
    - The message history
    - The maximum number of rounds
    """
    
    def __init__(self, topic: str, max_rounds: int = 1):
        """
        Initialize a new debate controller.
        
        Args:
            topic: The debate topic
            max_rounds: Maximum number of rebuttal rounds (default: 1)
        """
        self.topic = topic
        self.max_rounds = max_rounds
        self.round_number = 0
        self.turn = AgentTurn.PRO  # Pro agent (Ava) goes first
        self.messages: List[Dict[str, Any]] = []
        
        # Create a debate context for additional functionality
        self.context = DebateContext(topic)
        self.context.max_rounds = max_rounds
        
        # Add the initial topic message
        topic_message = DebateProtocol.topic_message(topic)
        self.add_message(topic_message)
    
    def next_agent(self) -> Tuple[AgentTurn, int]:
        """
        Determine which agent should go next based on the current state.
        
        Returns:
            A tuple of (agent_turn, round_number) indicating who goes next and in which round
        """
        # If debate is done, no more agents
        if self.turn == AgentTurn.DONE:
            return (AgentTurn.DONE, self.round_number)
        
        # Determine the next agent in the sequence
        if self.turn == AgentTurn.PRO:
            next_turn = AgentTurn.CON
            next_round = self.round_number
        elif self.turn == AgentTurn.CON:
            # Check if we're at the max rounds or still in initial arguments (round 0)
            if self.round_number == 0:
                # After initial arguments from both sides, go to moderator if no rebuttals requested
                if self.max_rounds == 0:
                    next_turn = AgentTurn.MOD
                    next_round = 0
                else:
                    # Otherwise move to first rebuttal round
                    next_turn = AgentTurn.PRO
                    next_round = 1
            elif self.round_number >= self.max_rounds:
                # If we've completed all rebuttal rounds, go to moderator
                next_turn = AgentTurn.MOD
                next_round = self.round_number
            else:
                # Continue with rebuttals
                next_turn = AgentTurn.PRO
                next_round = self.round_number + 1
        elif self.turn == AgentTurn.MOD:
            next_turn = AgentTurn.DONE
            next_round = self.round_number
        else:
            # Shouldn't happen, but just in case
            next_turn = AgentTurn.DONE
            next_round = self.round_number
        
        # Update the controller state
        self.turn = next_turn
        self.round_number = next_round
        
        return (next_turn, next_round)
    
    def add_message(self, message: Dict[str, Any]) -> None:
        """
        Add a message to the debate history.
        
        Args:
            message: A message formatted according to the DebateProtocol
        """
        # Validate the message format
        validated_message = DebateProtocol.parse_message(message)
        
        # Add to our message list
        self.messages.append(validated_message)
        
        # Also add to the context for additional functionality
        self.context.add_message(validated_message)
        
        # Update round number if the message has a round field
        if "round" in validated_message and validated_message["round"] > self.round_number:
            self.round_number = validated_message["round"]
    
    def get_latest_messages(self, n: int = 3) -> List[Dict[str, Any]]:
        """
        Get the n most recent messages.
        
        Args:
            n: Number of messages to retrieve (default: 3)
            
        Returns:
            List of the n most recent messages
        """
        return self.messages[-n:] if len(self.messages) >= n else self.messages[:]
    
    def get_all_messages(self) -> List[Dict[str, Any]]:
        """
        Get all messages in the debate history.
        
        Returns:
            List of all messages
        """
        return self.messages[:]
    
    def get_messages_by_type(self, message_type: MessageType) -> List[Dict[str, Any]]:
        """
        Get all messages of a specific type.
        
        Args:
            message_type: The type of message to filter by
            
        Returns:
            List of messages of the specified type
        """
        return self.context.get_messages_by_type(message_type)
    
    def get_messages_for_round(self, round_number: int) -> List[Dict[str, Any]]:
        """
        Get all messages for a specific round.
        
        Args:
            round_number: The round number to filter by
            
        Returns:
            List of messages from the specified round
        """
        return self.context.get_messages_for_round(round_number)
    
    def get_messages_for_agent(self, agent_id: str) -> List[Dict[str, Any]]:
        """
        Get all messages from a specific agent.
        
        Args:
            agent_id: The agent identifier to filter by
            
        Returns:
            List of messages from the specified agent
        """
        return self.context.get_messages_for_agent(agent_id)
    
    def get_debate_summary(self) -> Dict[str, Any]:
        """
        Get a summary of the debate state.
        
        Returns:
            Dictionary with debate metadata
        """
        return {
            "topic": self.topic,
            "current_round": self.round_number,
            "max_rounds": self.max_rounds,
            "current_turn": self.turn.value,
            "message_count": len(self.messages),
            "is_complete": self.turn == AgentTurn.DONE
        }
    
    def format_for_agent(self, agent_turn: AgentTurn) -> str:
        """
        Format the debate history in a way that's useful for the next agent.
        
        Args:
            agent_turn: Which agent will receive this context
            
        Returns:
            Formatted string with relevant context for the agent
        """
        formatted_context = [f"Debate topic: {self.topic}"]
        
        if agent_turn == AgentTurn.PRO and self.round_number == 0:
            # Initial Pro argument needs just the topic
            return "\n".join(formatted_context)
        
        if agent_turn == AgentTurn.CON and self.round_number == 0:
            # Initial Con argument needs the topic and Pro's initial argument
            pro_messages = self.context.get_messages_for_side("pro")
            if pro_messages:
                formatted_context.append("\nPro argument:")
                formatted_context.append(pro_messages[0]["content"])
            return "\n".join(formatted_context)
        
        if agent_turn == AgentTurn.PRO and self.round_number > 0:
            # Pro rebuttal needs the previous Con argument
            con_messages = self.context.get_messages_for_side("con")
            if con_messages and len(con_messages) >= self.round_number:
                formatted_context.append("\nCon argument to rebut:")
                formatted_context.append(con_messages[self.round_number-1]["content"])
            return "\n".join(formatted_context)
        
        if agent_turn == AgentTurn.CON and self.round_number > 0:
            # Con rebuttal needs the previous Pro rebuttal
            pro_messages = self.context.get_messages_for_side("pro")
            if pro_messages and len(pro_messages) > self.round_number:
                formatted_context.append("\nPro rebuttal to counter:")
                formatted_context.append(pro_messages[self.round_number]["content"])
            return "\n".join(formatted_context)
        
        if agent_turn == AgentTurn.MOD:
            # Moderator needs all arguments
            formatted_context.append("\nDebate arguments:")
            
            # Add initial arguments
            pro_messages = self.context.get_messages_for_side("pro")
            con_messages = self.context.get_messages_for_side("con")
            
            if pro_messages:
                formatted_context.append("\nInitial Pro argument:")
                formatted_context.append(pro_messages[0]["content"])
            
            if con_messages:
                formatted_context.append("\nInitial Con argument:")
                formatted_context.append(con_messages[0]["content"])
            
            # Add rebuttals for each round
            for round_num in range(1, self.round_number + 1):
                formatted_context.append(f"\nRound {round_num}:")
                
                if pro_messages and len(pro_messages) > round_num:
                    formatted_context.append(f"\nPro rebuttal (round {round_num}):")
                    formatted_context.append(pro_messages[round_num]["content"])
                
                if con_messages and len(con_messages) > round_num:
                    formatted_context.append(f"\nCon rebuttal (round {round_num}):")
                    formatted_context.append(con_messages[round_num]["content"])
            
            return "\n".join(formatted_context)
        
        # Default - just return the topic
        return "\n".join(formatted_context)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the controller state to a dictionary.
        
        Returns:
            Dictionary representation of the controller state
        """
        return {
            "topic": self.topic,
            "round_number": self.round_number,
            "turn": self.turn.value,
            "max_rounds": self.max_rounds,
            "messages": self.messages,
            "is_complete": self.turn == AgentTurn.DONE
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DebateController':
        """
        Create a controller from a dictionary.
        
        Args:
            data: Dictionary representation of controller state
            
        Returns:
            New DebateController instance
        """
        controller = cls(data["topic"], data["max_rounds"])
        controller.round_number = data["round_number"]
        controller.turn = AgentTurn(data["turn"])
        
        # Clear the default topic message
        controller.messages = []
        
        # Add all messages
        for message in data["messages"]:
            controller.add_message(message)
        
        return controller 