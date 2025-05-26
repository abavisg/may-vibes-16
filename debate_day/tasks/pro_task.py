from crewai import Task
# from agents.pro_agent import ava_agent # This import is no longer needed and causes an error

# Hardcoded topic for now - this will be overridden by create_debate_crew
topic = "Remote work is better than office work"

pro_debate_task = Task(
    description=f"Provide exactly one clear, focused argument supporting the topic: '{topic}'. Be direct and concise.",
    expected_output=(
        "A single, concise argument in favor of the topic, expressed in 1-2 sentences maximum."
    ),
    # agent=ava_agent # Agent is now assigned in debate_crew.py
)
