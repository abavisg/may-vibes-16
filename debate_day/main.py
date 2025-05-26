from crew.debate_crew import create_debate_crew
import os
import logging
from langchain_community.chat_models import ChatOllama
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
import litellm

# --- Basic Logging Setup ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s')
logger = logging.getLogger(__name__)

# Disable LiteLLM's provider list message
litellm.suppress_debug_info = True

# --- LLM Configuration for Ollama --- 
logger.info("Starting LLM configuration for ChatOllama...")
USE_HIGH_QUALITY_MODEL = True  # True for llama3, False for tinyllama
OLLAMA_BASE_URL = 'http://localhost:11434'

if USE_HIGH_QUALITY_MODEL:
    SELECTED_MODEL_NAME = 'llama3'
else:
    SELECTED_MODEL_NAME = 'tinyllama'

print(f"Configuring ChatOllama model: {SELECTED_MODEL_NAME} via {OLLAMA_BASE_URL}")

# Define the LLM configuration for ChatOllama
llm_config = {
    "base_url": OLLAMA_BASE_URL,
    "model": f"ollama/{SELECTED_MODEL_NAME}",  # Specify Ollama as the provider
    "temperature": 0.1,  # Lower temperature for more focused responses
    "callbacks": [StreamingStdOutCallbackHandler()],
    "streaming": True,  # Enable streaming for better responsiveness
    "request_timeout": 120,  # Increase timeout to 2 minutes
}

# Instantiate the ChatOllama model
ollama_llm = ChatOllama(**llm_config)
logger.info("ChatOllama instance created with StreamingStdOutCallbackHandler.")

# --- Minimal CrewAI Test --- 
def run_minimal_crewai_test():
    from agents.pro_agent import create_pro_agent
    from crewai import Crew, Task, Process

    logger.info("[Minimal Test] Creating minimalist Pro agent with ChatOllama...")
    try:
        # Pass the ChatOllama instance to the agent creation function
        minimal_ava = create_pro_agent(llm=ollama_llm) 
        logger.info("[Minimal Test] Minimalist Pro agent created.")

        minimal_task = Task(
            description="Your task is to respond with exactly one word: 'Hello'. Do not add any explanation or additional text.",
            expected_output="Hello",
            agent=minimal_ava
        )
        logger.info("[Minimal Test] Minimal task created.")

        minimal_crew = Crew(
            agents=[minimal_ava],
            tasks=[minimal_task],
            process=Process.sequential,
            verbose=True 
        )
        logger.info("[Minimal Test] Minimal crew created. Kicking off...")
        result = minimal_crew.kickoff()
        logger.info(f"[Minimal Test] Crew kickoff complete. Result: {result}")
    except Exception as e:
        logger.error(f"[Minimal Test] Error during minimal CrewAI test: {e}", exc_info=True)

def run_debate():
    logger.info("run_debate function started.")
    print("\n🚀 Welcome to Debate Day! 🚀")
    print("------------------------------------")
    
    topic = input("Please enter the topic for the debate: ")
    
    if not topic.strip():
        logger.warning("No topic entered. Exiting run_debate.")
        print("No topic entered. Exiting.")
        return

    logger.info(f"Debate topic: '{topic}'")
    print(f"\nOkay, setting up a debate on the topic: '{topic}'\n")

    logger.info("Creating debate crew...")
    debate_squad = create_debate_crew(topic=topic, llm=ollama_llm)
    logger.info("Debate crew created.")

    print("\nKicking off the debate...\n")
    logger.info("Kicking off crew...")
    try:
        result = debate_squad.kickoff()
        logger.info("Crew kickoff complete. Result received.")

        print("\n------------------------------------")
        print("🏁 Debate Concluded! 🏁")
        print("------------------------------------\n")
        print("Final Output (Moderator's Assessment):\n")
        print(result)
    except Exception as e:
        logger.error(f"Exception during crew kickoff: {e}", exc_info=True)
        print(f"\nAn error occurred during the debate: {e}")
        print(f"\nPlease ensure your Ollama server is running and the specified model ('{SELECTED_MODEL_NAME}') is available.")
        print(f"CrewAI is configured to connect to Ollama via: {OLLAMA_BASE_URL} for model '{SELECTED_MODEL_NAME}'.")
        print("You can pull models using 'ollama pull <model_name>' (e.g., 'ollama pull tinyllama').")
        print("If issues persist, check the logs for detailed error messages.")
    logger.info("run_debate function finished.")

if __name__ == "__main__":
    logger.info("Script started as main.")
    run_minimal_crewai_test()
    logger.info("Script finished.")
