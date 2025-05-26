from crew.debate_crew import create_debate_crew
import os
import logging
from langchain_community.chat_models import ChatOllama
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
import litellm

# --- Basic Logging Setup ---
# Configure logging before anything else
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s')

# Completely suppress all third-party loggers
for logger_name in ['litellm', 'httpx', 'httpcore', 'litellm.utils', 'litellm.cost_calculator']:
    third_party_logger = logging.getLogger(logger_name)
    third_party_logger.setLevel(logging.ERROR)
    third_party_logger.addHandler(logging.NullHandler())
    third_party_logger.propagate = False

# Get our logger
logger = logging.getLogger(__name__)

# Disable LiteLLM's provider list message and cost calculation
litellm.suppress_debug_info = True
litellm.success_callback = None  # Disable success callback which triggers cost calculation
os.environ["DISABLE_COST_CALCULATION"] = "true"
os.environ["LITELLM_SUPPRESS_COST_CALCULATION"] = "true"

# --- LLM Configuration for Ollama --- 
logger.info("Starting LLM configuration for ChatOllama...")
USE_HIGH_QUALITY_MODEL = True  # True for llama3, False for tinyllama
OLLAMA_BASE_URL = 'http://localhost:11434'
SELECTED_MODEL_NAME = 'llama3' if USE_HIGH_QUALITY_MODEL else 'tinyllama'

print(f"Configuring ChatOllama model: {SELECTED_MODEL_NAME} via {OLLAMA_BASE_URL}")

# Define the LLM configuration for ChatOllama
llm_config = {
    "base_url": OLLAMA_BASE_URL,
    "model": f"ollama/{SELECTED_MODEL_NAME}",
    "temperature": 0.1,  # Lower temperature for more focused responses
    "callbacks": [StreamingStdOutCallbackHandler()],
    "streaming": True,  # Enable streaming for better responsiveness
    "request_timeout": 120,  # Increase timeout to 2 minutes
}

# Instantiate the ChatOllama model
ollama_llm = ChatOllama(**llm_config)
logger.info("ChatOllama instance created with StreamingStdOutCallbackHandler.")

def run_debate():
    """Main function to run the debate application."""
    print("\n" + "="*50)
    print("🎯 Welcome to Debate Day! 🎯")
    print("="*50 + "\n")
    
    while True:
        topic = input("Enter your debate topic (or 'q' to quit): ").strip()
        
        if topic.lower() == 'q':
            print("\nThanks for using Debate Day! Goodbye! 👋\n")
            break
            
        if not topic:
            print("\n⚠️  Please enter a valid topic!\n")
            continue

        print("\n" + "-"*50)
        print(f"📢 Starting debate on: '{topic}'")
        print("-"*50 + "\n")

        try:
            # Create and run the debate
            debate_squad = create_debate_crew(topic=topic, llm=ollama_llm)
            print("\n🎬 The debate begins...\n")
            result = debate_squad.kickoff()

            # Display results
            print("\n" + "="*50)
            print("🏁 Debate Concluded!")
            print("="*50 + "\n")
            print("📋 Moderator's Assessment:\n")
            print(result)
            print("\n" + "-"*50 + "\n")
            
        except Exception as e:
            logger.error(f"Error during debate: {e}", exc_info=True)
            print(f"\n❌ An error occurred: {e}")
            print(f"\n💡 Troubleshooting tips:")
            print(f"  • Check if Ollama server is running at {OLLAMA_BASE_URL}")
            print(f"  • Ensure model '{SELECTED_MODEL_NAME}' is available")
            print(f"  • Try: ollama pull {SELECTED_MODEL_NAME}")
            print("\n")

if __name__ == "__main__":
    try:
        run_debate()
    except KeyboardInterrupt:
        print("\n\nDebate Day closed by user. Goodbye! 👋\n")
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        print(f"\n❌ Unexpected error: {e}\n")
