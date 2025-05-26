import logging
from crewai import Agent
from protocol import DebateProtocol, MessageType

logger = logging.getLogger(__name__)

def create_pro_agent(llm=None):
    """Creates the Pro agent (Ava) with the specified LLM."""
    
    if llm is None:
        raise ValueError("LLM instance must be provided for agent creation")

    agent = Agent(
        role='Debate Pro Agent',
        goal='Present compelling arguments in favor of the given topic',
        backstory="""You are Ava, an expert debater known for constructing clear, 
        focused arguments. You excel at finding strong supporting evidence for your positions.""",
        allow_delegation=False,
        llm=llm,
        tools=[],  # No tools needed for basic debate
        verbose=True,
        max_iterations=1,  # We want a single, focused response
        system_message="""You are participating in a formal debate using the Model Context Protocol.
        Your role is to argue IN FAVOR of the topic provided in your task.
        
        For initial arguments:
        - Provide exactly one clear, focused argument supporting the position in 1-2 sentences maximum.
        - Be direct, concise, and persuasive.
        
        For rebuttals:
        - Carefully review the Con agent's previous argument.
        - Address specific weaknesses in their reasoning or evidence.
        - Reinforce your position with additional support.
        - Keep your rebuttal focused and limited to 1-2 sentences.
        
        All your responses will be formatted according to the Model Context Protocol.
        """
    )
    
    return agent

def format_pro_response(content, agent_id="ava", round_number=0):
    """Format the Pro agent's response according to the Model Context Protocol."""
    return DebateProtocol.argument_message(
        content=content,
        side="pro",
        agent_id=agent_id,
        round_number=round_number
    )
