import logging
from crewai import Agent

logger = logging.getLogger(__name__)

def create_con_agent(llm=None):
    """Creates the Con agent (Ben) with the specified LLM."""
    logger.info("create_con_agent function called.")
    
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
        system_message="""You are participating in a formal debate about whether artificial intelligence should be regulated by governments.
        Your role is to argue AGAINST government regulation of AI.
        After reviewing the Pro agent's argument, provide exactly one clear, focused counter-argument in 1-2 sentences maximum.
        Address their specific points directly and explain why their position is flawed.
        Be direct, concise, and persuasive.
        """
    )
    
    logger.info("Con agent created.")
    return agent
