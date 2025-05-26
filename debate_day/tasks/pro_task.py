from crewai import Task
# from agents.pro_agent import ava_agent # This import is no longer needed and causes an error

# Hardcoded topic for now - this will be overridden by create_debate_crew
topic = "Remote work is better than office work"

pro_debate_task = Task(
    description=(
        "This is a debate about whether artificial intelligence should be regulated by governments. "
        "Your role is to argue IN FAVOR of government regulation of AI. "
        "Provide exactly one clear, focused argument supporting the topic: 'Should artificial intelligence be regulated by governments?'. "
        "Be direct and concise, presenting your argument in 1-2 sentences that are compelling and evidence-based."
    ),
    expected_output=(
        "A single, concise argument in favor of the topic, expressed in 1-2 sentences maximum."
    ),
    # agent=ava_agent # Agent is now assigned in debate_crew.py
)
