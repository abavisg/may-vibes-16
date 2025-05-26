from crewai import Task
# from agents.con_agent import ben_agent # This import is no longer needed
from tasks.pro_task import pro_debate_task # To access the context from pro_debate_task

# The topic is implicitly taken from the context of pro_debate_task

con_debate_task = Task(
    description=(
        "Provide exactly one clear, focused counter-argument to the Pro agent's point. "
        "Address their argument directly and be concise."
    ),
    expected_output=(
        "A single, concise counter-argument that directly addresses the Pro agent's point, "
        "expressed in 1-2 sentences maximum."
    ),
    # agent=ben_agent, # Agent is now assigned in debate_crew.py
    context=[pro_debate_task]
)
