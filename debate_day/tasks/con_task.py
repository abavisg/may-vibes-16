from crewai import Task
# from agents.con_agent import ben_agent # This import is no longer needed
from tasks.pro_task import pro_debate_task # To access the context from pro_debate_task

# The topic is implicitly taken from the context of pro_debate_task

con_debate_task = Task(
    description=(
        "Respond to the Pro agent's point with a counter-argument. "
        "Address the point directly and provide a clear refutation."
    ),
    expected_output=(
        "A counter-argument, directly addressing the Pro agent's point. "
        "The counter-argument should be well-reasoned and clearly articulated."
    ),
    # agent=ben_agent, # Agent is now assigned in debate_crew.py
    context=[pro_debate_task]
)
