from crewai import Crew, Process
# Import agent creation functions
from agents.pro_agent import create_pro_agent
from agents.con_agent import create_con_agent
from agents.mod_agent import create_mod_agent

# Import task blueprints (they will be assigned agents dynamically)
from tasks.pro_task import pro_debate_task, pro_rebuttal_task
from tasks.con_task import con_debate_task, con_rebuttal_task
from tasks.mod_task import moderator_task

import logging
import copy

logger = logging.getLogger(__name__)

def create_debate_crew(llm=None, num_rebuttals=1):
    """Creates and configures the debate crew.
       Agents will use the provided LLM instance.
       
       Args:
           llm: The language model to use for the agents
           num_rebuttals: Number of rebuttals each side should have (default: 1)
    """

    logger.info("create_debate_crew called")
    if llm is None:
        logger.warning("No LLM provided to create_debate_crew. Agents may not function properly.")
        
    # Create agents with the provided LLM
    ava = create_pro_agent(llm=llm)
    ben = create_con_agent(llm=llm)
    mia = create_mod_agent(llm=llm)
    
    # Assign agents to tasks
    pro_debate_task.agent = ava
    con_debate_task.agent = ben
    moderator_task.agent = mia
    
    # Set up initial task dependencies
    con_debate_task.context = [pro_debate_task]  # Con needs Pro's initial argument
    
    # Create list of all tasks
    all_tasks = [pro_debate_task, con_debate_task]
    
    # Dictionary to track the latest tasks for each side
    latest_tasks = {
        "pro": pro_debate_task,
        "con": con_debate_task
    }
    
    # Add rebuttal tasks based on the user's selection
    all_rebuttal_tasks = []
    
    for rebuttal_round in range(1, num_rebuttals + 1):
        logger.info(f"Setting up rebuttal round {rebuttal_round}")
        
        # Create a pro rebuttal task for this round
        pro_rebuttal = copy.deepcopy(pro_rebuttal_task)
        pro_rebuttal.agent = ava
        pro_rebuttal.description += f" (Round {rebuttal_round})"
        
        # The pro rebuttal needs context from all previous tasks
        pro_rebuttal.context = list(all_tasks)
        
        # Add the pro rebuttal to our lists
        all_tasks.append(pro_rebuttal)
        all_rebuttal_tasks.append(pro_rebuttal)
        latest_tasks["pro"] = pro_rebuttal
        
        # Create a con rebuttal task for this round
        con_rebuttal = copy.deepcopy(con_rebuttal_task)
        con_rebuttal.agent = ben
        con_rebuttal.description += f" (Round {rebuttal_round})"
        
        # The con rebuttal needs context from all previous tasks
        con_rebuttal.context = list(all_tasks)
        
        # Add the con rebuttal to our lists
        all_tasks.append(con_rebuttal)
        all_rebuttal_tasks.append(con_rebuttal)
        latest_tasks["con"] = con_rebuttal
        
    # The moderator needs context from all previous tasks
    moderator_task.context = list(all_tasks)
    
    # Add moderator task to the list
    all_tasks.append(moderator_task)
    
    logger.info(f"Configured debate with {len(all_tasks)} total tasks")
    
    debate_crew = Crew(
        agents=[ava, ben, mia],
        tasks=all_tasks,
        process=Process.sequential,  # Tasks must run in sequence
        verbose=True 
    )
    logger.info("Crew object instantiated.")
    return debate_crew
