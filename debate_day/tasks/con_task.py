from crewai import Task
from agents.con_agent import ben_agent # Assuming con_agent.py is in agents/
from tasks.pro_task import pro_debate_task # To access the context from pro_debate_task

# The topic is implicitly taken from the context of pro_debate_task

con_debate_task = Task(
    description=(
        "Respond to each of the Pro points with counter-arguments. "
        "Address each point directly and provide clear refutations."
    ),
    expected_output=(
        "A list of counter-arguments, directly addressing each of the Pro agent's points. "
        "Each counter-argument should be well-reasoned and clearly articulated."
    ),
    agent=ben_agent,
    context=[pro_debate_task] # Make this task dependent on the output of pro_debate_task
)
