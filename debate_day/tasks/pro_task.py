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

# Add a rebuttal task for the Pro agent to respond to the Con agent's argument
pro_rebuttal_task = Task(
    description=(
        "Review the Con agent's argument carefully. "
        "This is your opportunity to rebut their counter-argument with your own follow-up point. "
        "Your rebuttal should directly address the flaws or weaknesses in their argument. "
        "Be focused and precise, offering a compelling response that strengthens your original position. "
        "Your rebuttal should be 1-2 sentences maximum."
    ),
    expected_output=(
        "A concise, focused rebuttal that directly addresses the Con agent's argument, "
        "expressed in 1-2 sentences maximum."
    ),
    # agent is assigned in debate_crew.py
)
