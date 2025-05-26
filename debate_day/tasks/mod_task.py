from crewai import Task
# from agents.mod_agent import mia_agent # This import is no longer needed
from tasks.pro_task import pro_debate_task
from tasks.con_task import con_debate_task

moderator_task = Task(
    description=(
        "You are moderating a multi-round debate where agents have presented arguments and possibly multiple rebuttals.\n\n"
        "Evaluate the entire debate concisely using this structure:\n"
        "1. Initial Pro argument evaluation (1 sentence)\n"
        "2. Initial Con argument evaluation (1 sentence)\n"
        "3. For each rebuttal round:\n"
        "   - Pro rebuttal evaluation (1 sentence)\n"
        "   - Con rebuttal evaluation (1 sentence)\n"
        "4. Winner declaration with brief rationale (1-2 sentences)\n\n"
        "Consider all arguments and rebuttals in your final decision. Base your evaluation on the strength of reasoning, evidence, and persuasiveness."
    ),
    expected_output=(
        "A structured evaluation that covers:\n"
        "1. Pro initial argument evaluation\n"
        "2. Con initial argument evaluation\n"
        "3. Each rebuttal evaluation (organized by round)\n"
        "4. Winner: [Ava (Pro) or Ben (Con)] - [brief rationale]"
    ),
    # agent=mia_agent, # Agent is now assigned in debate_crew.py
    context=[pro_debate_task, con_debate_task]
) 