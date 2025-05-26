from crewai import Crew, Process
# Import agent creation functions
from agents.pro_agent import create_pro_agent
from agents.con_agent import create_con_agent
from agents.mod_agent import create_mod_agent

# Import task blueprints (they will be assigned agents dynamically)
from tasks.pro_task import pro_debate_task
from tasks.con_task import con_debate_task
from tasks.mod_task import moderator_task

def create_debate_crew(topic: str):
    """Creates and configures the debate crew with a dynamic topic.
       Agents will use global LLM configuration (e.g., from environment variables)."""

    # Create agents (they will use the LLM configured globally via env vars)
    ava = create_pro_agent()
    ben = create_con_agent()
    mia = create_mod_agent()

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

    debate_crew = Crew(
        agents=[ava, ben, mia],
        tasks=[pro_debate_task, con_debate_task, moderator_task],
        process=Process.sequential,
        verbose=True 
    )
    return debate_crew
