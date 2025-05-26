from crewai import Task
# from agents.mod_agent import mia_agent # This import is no longer needed
from tasks.pro_task import pro_debate_task
from tasks.con_task import con_debate_task

moderator_task = Task(
    description=(
        "Evaluate the debate concisely using this structure:\n"
        "1. Pro argument strength (1 sentence)\n"
        "2. Con argument strength (1 sentence)\n"
        "3. Winner declaration with brief rationale (1-2 sentences)"
    ),
    expected_output=(
        "A structured evaluation with exactly three parts:\n"
        "1. Pro evaluation (1 sentence)\n"
        "2. Con evaluation (1 sentence)\n"
        "3. Winner: [Ava (Pro) or Ben (Con)] - [brief rationale]"
    ),
    # agent=mia_agent, # Agent is now assigned in debate_crew.py
    context=[pro_debate_task, con_debate_task]
) 