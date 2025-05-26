import logging
from crewai import Agent
from protocol import DebateProtocol, MessageType

logger = logging.getLogger(__name__)

def create_mod_agent(llm=None):
    """Creates the Moderator agent (Mia) with the specified LLM."""
    
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
        system_message="""You are moderating a formal debate that may include multiple rounds of rebuttals.
        Ava (Pro) is arguing IN FAVOR of the topic.
        Ben (Con) is arguing AGAINST the topic.
        
        Your task is to evaluate all arguments and rebuttals objectively and determine which side presented the stronger case.
        
        Format your evaluation with the following structure:
        1. Initial Pro argument evaluation (1 sentence)
        2. Initial Con argument evaluation (1 sentence)
        3. For each rebuttal round:
           - Pro rebuttal evaluation (1 sentence)
           - Con rebuttal evaluation (1 sentence)
        4. Winner declaration with brief rationale (1-2 sentences)
        
        Be fair, impartial, and focus on the quality of arguments rather than your personal opinion on the topic.
        
        Your evaluation will be formatted according to the Model Context Protocol for standardized communication.
        """
    )
    
    return agent

def format_mod_evaluation(content, winner, agent_id="mia"):
    """Format the Moderator agent's evaluation according to the Model Context Protocol."""
    return DebateProtocol.evaluation_message(
        content=content,
        winner=winner,
        agent_id=agent_id
    ) 