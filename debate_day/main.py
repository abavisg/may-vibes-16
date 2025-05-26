import os
import logging
from crewai import LLM, Agent, Crew, Process, Task
from crew.debate_crew import create_debate_crew
from tasks.pro_task import pro_debate_task
from tasks.con_task import con_debate_task

# --- Basic Logging Setup ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s')
logger = logging.getLogger(__name__)

# --- Disable noisy loggers ---
for logger_name in ['httpx', 'httpcore']:
    logging.getLogger(logger_name).setLevel(logging.WARNING)

# --- LLM Configuration for Ollama --- 
logger.info("Starting LLM configuration for Ollama...")
OLLAMA_BASE_URL = 'http://localhost:11434'
MODEL_NAME = 'llama3'

logger.info(f"Configuring Ollama model: {MODEL_NAME} via {OLLAMA_BASE_URL}")

# Create the Ollama LLM instance using the correct CrewAI LLM class
ollama_llm = LLM(
    model=f"ollama/{MODEL_NAME}",
    base_url=OLLAMA_BASE_URL,
    temperature=0.1,  # Lower temperature for more focused responses
)

def get_user_topic():
    """Prompt the user for a debate topic."""
    print("\n=== Debate Day ===")
    print("Enter a debate topic for the AI agents to discuss.")
    print("Example: 'Did we ever go to the moon?'")
    user_topic = input("\nDebate topic: ")
    
    # Provide a default if the user enters nothing
    if not user_topic.strip():
        user_topic = "Did we ever go to the moon?"
        print(f"Using default topic: {user_topic}")
    
    return user_topic

def update_task_descriptions(topic):
    """Update the task descriptions with the user-provided topic."""
    # Update Pro task description
    pro_debate_task.description = (
        f"This is a debate about {topic}. "
        f"Your role is to argue IN FAVOR of this position. "
        f"Provide exactly one clear, focused argument supporting the topic. "
        f"Be direct and concise, presenting your argument in 1-2 sentences that are compelling and evidence-based."
    )
    
    # Update Con task description
    con_debate_task.description = (
        f"This is a debate about {topic}. "
        f"Your role is to argue AGAINST this position. "
        f"Review the Pro agent's argument carefully and then provide exactly one clear, focused counter-argument. "
        f"Your counter-argument should directly address and oppose the Pro agent's position. "
        f"Be concise and specific, explaining why the Pro agent's viewpoint is flawed or incomplete. "
        f"Your response should be 1-2 sentences long and present a compelling opposing perspective."
    )

def run_debate():
    """Run the main debate application."""
    logger.info("Starting debate application...")
    try:
        # Get debate topic from user
        debate_topic = get_user_topic()
        logger.info(f"Debate topic: {debate_topic}")
        
        # Update task descriptions with the user-provided topic
        update_task_descriptions(debate_topic)
        logger.info("Task descriptions updated with user topic.")
        
        # Create the debate crew with our configured LLM
        crew = create_debate_crew(llm=ollama_llm)
        logger.info("Debate crew created successfully.")

        # Run the debate
        result = crew.kickoff()
        logger.info("Debate completed successfully.")
        return result

    except Exception as e:
        logger.error(f"Error running debate: {e}")
        raise

if __name__ == "__main__":
    try:
        # Run the actual debate
        logger.info("Starting main debate application...")
        debate_result = run_debate()
        logger.info("Debate completed.")
        print("\nDebate Result:")
        print(debate_result)

    except Exception as e:
        logger.error(f"Application error: {e}")
        raise
