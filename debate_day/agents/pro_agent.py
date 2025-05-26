import logging
from crewai import Agent

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
        system_message="""You are participating in a formal debate.
        Your role is to argue IN FAVOR of the topic provided in your task.
        Provide exactly one clear, focused argument supporting this position in 1-2 sentences maximum.
        Be direct, concise, and persuasive.
        """
    )
    
    return agent
