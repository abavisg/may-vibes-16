from crewai import Agent

def create_con_agent():
    return Agent(
        role='DebateBot Con Agent',
        goal='Argue against the topic',
        backstory=(
            "Ben is a seasoned contrarian who values tradition and proven systems. "
            "He is critical, polite, and sharp in his counter-arguments."
        ),
        verbose=True,
        allow_delegation=False
    )
