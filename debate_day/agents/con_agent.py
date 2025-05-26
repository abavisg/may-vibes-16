import logging
from crewai import Agent
from protocol import DebateProtocol, MessageType

logger = logging.getLogger(__name__)

def create_con_agent(llm=None):
    """Creates the Con agent (Ben) with the specified LLM."""
    
    if llm is None:
        raise ValueError("LLM instance must be provided for agent creation")

    agent = Agent(
        role='Debate Con Agent',
        goal='Present compelling counter-arguments against the given topic',
        backstory="""You are Ben, a skilled debater known for identifying flaws in arguments 
        and presenting strong counter-points. You excel at critical analysis and logical reasoning.""",
        allow_delegation=False,
        llm=llm,
        tools=[],  # No tools needed for basic debate
        verbose=True,
        max_iterations=1,  # We want a single, focused response
        system_message="""You are participating in a formal debate using the Model Context Protocol.
        Your role is to argue AGAINST the topic provided in your task.
        
        For initial arguments:
        - After reviewing the Pro agent's argument, provide exactly one clear, focused counter-argument.
        - Address their specific points directly and explain why their position is flawed.
        - Be direct, concise, and persuasive in 1-2 sentences maximum.
        
        For rebuttals:
        - Carefully review the Pro agent's previous rebuttal.
        - Identify weaknesses in their reasoning or evidence.
        - Strengthen your position with additional support.
        - Keep your counter-rebuttal focused and limited to 1-2 sentences.
        
        All your responses will be formatted according to the Model Context Protocol.
        """
    )
    
    return agent

def format_con_response(content, agent_id="ben", round_number=0):
    """Format the Con agent's response according to the Model Context Protocol."""
    return DebateProtocol.argument_message(
        content=content,
        side="con",
        agent_id=agent_id,
        round_number=round_number
    )
