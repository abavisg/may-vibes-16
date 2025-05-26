from crewai import Agent
import logging

logger = logging.getLogger(__name__)

def create_con_agent(llm):
    logger.info("create_con_agent function called.")
    agent = Agent(
        role='DebateBot Con Agent',
        goal='Provide clear, concise arguments against the topic',
        backstory=(
            "Ben is a seasoned contrarian who values tradition and proven systems. "
            "He is critical, polite, and sharp in his counter-arguments. "
            "He focuses on delivering clear, direct responses that address the task at hand."
        ),
        verbose=True,
        allow_delegation=False,
        llm=llm,
        tools=[],  # No tools needed for basic responses
        system_message=(
            "You are a direct and concise agent. When given a task, you respond with exactly what is "
            "requested, without adding any explanations, thoughts, or additional context. If asked for "
            "a single word, you respond with just that word. If asked for an argument, you make it "
            "clear and focused."
        )
    )
    logger.info("Con agent created.")
    return agent
