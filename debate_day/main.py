import os
import logging
from crewai import LLM, Agent, Crew, Process, Task
from crew.debate_crew import create_debate_crew
from tasks.pro_task import pro_debate_task

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

def run_debate():
    """Run the main debate application."""
    logger.info("Starting debate application...")
    try:
        # Define the debate topic
        debate_topic = "Should artificial intelligence be regulated by governments?"
        logger.info(f"Debate topic: {debate_topic}")
        
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
