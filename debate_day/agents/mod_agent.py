import logging
from crewai import Agent

logger = logging.getLogger(__name__)

def create_mod_agent(llm=None):
    """Creates the Moderator agent (Mia) with the specified LLM."""
    logger.info("create_mod_agent function called.")
    
    if llm is None:
        raise ValueError("LLM instance must be provided for agent creation")

    agent = Agent(
        role='Debate Moderator',
        goal='Evaluate arguments from both sides and determine the winner based on logic and evidence',
        backstory="""You are Mia, an experienced debate moderator known for fair and insightful analysis. 
        You excel at evaluating arguments objectively and providing clear, structured assessments.""",
        allow_delegation=False,
        llm=llm,
        tools=[],  # No tools needed for basic debate
        verbose=True,
        max_iterations=1,  # We want a single, focused response
        system_message="""You are moderating a formal debate about whether artificial intelligence should be regulated by governments.
        Ava (Pro) is arguing IN FAVOR of government regulation of AI.
        Ben (Con) is arguing AGAINST government regulation of AI.
        Your task is to evaluate both arguments objectively and determine which one is stronger based on logic, evidence, and persuasiveness.
        Format your evaluation in exactly three parts:
        1. Pro argument strength (1 sentence)
        2. Con argument strength (1 sentence)
        3. Winner declaration with brief rationale (1-2 sentences)
        """
    )
    
    logger.info("Moderator agent created.")
    return agent 