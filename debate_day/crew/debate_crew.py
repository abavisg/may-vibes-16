from crewai import Crew, Process
# Import agent creation functions
from agents.pro_agent import create_pro_agent
from agents.con_agent import create_con_agent
from agents.mod_agent import create_mod_agent

# Import task blueprints (they will be assigned agents dynamically)
from tasks.pro_task import pro_debate_task
from tasks.con_task import con_debate_task
from tasks.mod_task import moderator_task

import logging

logger = logging.getLogger(__name__)

def create_debate_crew(topic: str, llm=None):
    """Creates and configures the debate crew with a dynamic topic.
       Agents will use the provided LLM instance."""

    logger.info(f"create_debate_crew called with topic: '{topic}'")
    if llm is None:
        logger.warning("No LLM provided to create_debate_crew. Agents may not function properly.")
        
    # Create agents with the provided LLM
    ava = create_pro_agent(llm=llm)
    ben = create_con_agent(llm=llm)
    mia = create_mod_agent(llm=llm)

    logger.info("Agents created: Ava, Ben, Mia.")

    # Dynamically update the pro_debate_task's description with the topic
    pro_debate_task.description = (
        f"Give 1 brief point supporting the topic: '{topic}'. Keep it concise."
    )
    # Assign agents to tasks
    pro_debate_task.agent = ava
    con_debate_task.agent = ben
    moderator_task.agent = mia
    
    # Ensure context is still set for con_debate_task and moderator_task
    # This should already be the case from their definitions but good to be mindful
    con_debate_task.context = [pro_debate_task]
    moderator_task.context = [pro_debate_task, con_debate_task]

    logger.info("Tasks configured and agents assigned.")
    
    debate_crew = Crew(
        agents=[ava, ben, mia],
        tasks=[pro_debate_task, con_debate_task, moderator_task],
        process=Process.sequential,
        verbose=True 
    )
    logger.info("Crew object instantiated.")
    return debate_crew
