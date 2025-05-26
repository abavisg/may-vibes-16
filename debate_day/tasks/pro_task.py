from crewai import Task
from agents.pro_agent import ava_agent # Assuming pro_agent.py is in agents/

# Hardcoded topic for now
topic = "Remote work is better than office work"

pro_debate_task = Task(
    description=f"Give 3 strong points supporting the topic: '{topic}'. Focus on clarity and strong reasoning.",
    expected_output=(
        "A list of 3 distinct and well-reasoned arguments in favor of the topic. Each argument should be clearly stated."
    ),
    agent=ava_agent
)
