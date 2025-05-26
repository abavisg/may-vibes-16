from crewai import Crew, Process
from agents.pro_agent import ava_agent
from agents.con_agent import ben_agent
from agents.mod_agent import mia_agent
from tasks.pro_task import pro_debate_task
from tasks.con_task import con_debate_task
from tasks.mod_task import moderator_task

def create_debate_crew(topic: str):
    """Creates and configures the debate crew with a dynamic topic, including a moderator."""

    # Update the pro_debate_task's description with the dynamic topic provided
    # Note: This modifies the imported task instance. 
    # For multiple debates in a single script run with different topics, 
    # a factory pattern for tasks might be more robust, but for a single debate 
    # per run, this is straightforward.
    pro_debate_task.description = (
        f"Give 3 strong points supporting the topic: '{topic}'. "
        f"Focus on clarity and strong reasoning."
    )

    # The con_debate_task and moderator_task use context from pro_debate_task, 
    # so their descriptions do not need explicit topic injection here.

    debate_crew = Crew(
        agents=[ava_agent, ben_agent, mia_agent],
        tasks=[pro_debate_task, con_debate_task, moderator_task],
        process=Process.sequential,  # Tasks will run in the order provided
        verbose=2  # For detailed output of the crew's execution
    )
    return debate_crew
