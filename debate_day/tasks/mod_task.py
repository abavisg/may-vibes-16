from crewai import Task
from agents.mod_agent import mia_agent
from tasks.pro_task import pro_debate_task
from tasks.con_task import con_debate_task

moderator_task = Task(
    description=(
        "Analyze the preceding debate between the Pro and Con agents. Evaluate their arguments based on structure, "
        "clarity, and logical consistency. Consider the relevance of their points to the original topic. "
        "Based on your analysis, determine which agent presented a more compelling case."
    ),
    expected_output=(
        "A summary of the debate, an evaluation of each agent's performance (Ava - Pro, Ben - Con), "
        "a declared winner (either 'Ava (Pro)' or 'Ben (Con)'), and a clear rationale for your decision. "
        "The rationale should highlight specific strengths and weaknesses observed in the arguments."
    ),
    agent=mia_agent,
    context=[pro_debate_task, con_debate_task]  # Mia needs to see both sides of the debate
) 