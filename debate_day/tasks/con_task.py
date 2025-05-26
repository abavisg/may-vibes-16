from crewai import Task
# from agents.con_agent import ben_agent # This import is no longer needed
from tasks.pro_task import pro_debate_task # To access the context from pro_debate_task

# The topic is implicitly taken from the context of pro_debate_task

con_debate_task = Task(
    description=(
        "This is a debate about whether artificial intelligence should be regulated by governments. "
        "Your role is to argue AGAINST government regulation of AI. "
        "Review the Pro agent's argument carefully and then provide exactly one clear, focused counter-argument. "
        "Your counter-argument should directly address and oppose the Pro agent's position. "
        "Be concise and specific, explaining why the Pro agent's viewpoint is flawed or incomplete. "
        "Your response should be 1-2 sentences long and present a compelling opposing perspective."
    ),
    expected_output=(
        "A single, concise counter-argument that directly addresses and opposes the Pro agent's point, "
        "expressed in 1-2 sentences maximum."
    ),
    # agent=ben_agent, # Agent is now assigned in debate_crew.py
    context=[pro_debate_task]
)

# Add a rebuttal task for the Con agent to respond to the Pro agent's rebuttal
con_rebuttal_task = Task(
    description=(
        "Review the Pro agent's rebuttal to your initial argument. "
        "This is your final opportunity to strengthen your position with a targeted counter-rebuttal. "
        "Your counter-rebuttal should address the weaknesses in the Pro agent's rebuttal and "
        "reinforce your original argument against the topic. "
        "Be focused and precise, delivering your strongest point in a compelling way. "
        "Your counter-rebuttal should be 1-2 sentences maximum."
    ),
    expected_output=(
        "A concise, focused counter-rebuttal that directly addresses the Pro agent's rebuttal, "
        "expressed in 1-2 sentences maximum."
    ),
    # agent is assigned in debate_crew.py
)
