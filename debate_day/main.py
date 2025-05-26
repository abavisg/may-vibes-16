from crew.debate_crew import create_debate_crew
import os
# import langchain # No longer needed
# from langchain_community.chat_models import ChatOllama # No longer needed

# --- LLM Configuration for Ollama via Environment Variables ---
# CrewAI (via LiteLLM) will use these to configure Ollama.
USE_HIGH_QUALITY_MODEL = False  # True for llama3, False for tinyllama

OLLAMA_API_BASE_V1 = 'http://localhost:11434/v1' # For OPENAI_API_BASE

if USE_HIGH_QUALITY_MODEL:
    SELECTED_MODEL_NAME = 'llama3'
else:
    SELECTED_MODEL_NAME = 'tinyllama'

print(f"Configuring Ollama model via environment variables: {SELECTED_MODEL_NAME} via {OLLAMA_API_BASE_V1}")

# Set environment variables for CrewAI/LiteLLM to use Ollama
os.environ["OPENAI_API_BASE"] = OLLAMA_API_BASE_V1
os.environ["OPENAI_MODEL_NAME"] = SELECTED_MODEL_NAME
os.environ["OPENAI_API_KEY"] = 'ollama'  # Required, can be any non-empty string for Ollama

# For more detailed logs from LiteLLM if issues persist:
# os.environ["LITELLM_DEBUG"] = "1"
# ---

# llm_config and ollama_llm instance are no longer needed here
# llm_config = { ... }
# ollama_llm = ChatOllama(**llm_config)

# langchain.debug = True # No longer needed as we are not using ChatOllama directly

def run_debate():
    """
    Prompts the user for a debate topic, creates and runs the debate crew,
    and prints the final output.
    """
    print("\n🚀 Welcome to Debate Day! 🚀")
    print("------------------------------------")
    
    topic = input("Please enter the topic for the debate: ")
    
    if not topic.strip():
        print("No topic entered. Exiting.")
        return

    print(f"\nOkay, setting up a debate on the topic: '{topic}'\n")

    # Create the debate crew (it will use the globally configured LLM)
    debate_squad = create_debate_crew(topic=topic)

    print("\nKicking off the debate...\n")
    try:
        result = debate_squad.kickoff()

        print("\n------------------------------------")
        print("🏁 Debate Concluded! 🏁")
        print("------------------------------------\n")
        print("Final Output (Moderator's Assessment):\n")
        print(result)
    except Exception as e:
        print(f"\nAn error occurred during the debate: {e}")
        print("\nPlease ensure your Ollama server is running and the specified model ('{SELECTED_MODEL_NAME}') is available.")
        print(f"CrewAI is configured to connect to Ollama via: {OLLAMA_API_BASE_V1} for model '{SELECTED_MODEL_NAME}'.")
        print("You can pull models using 'ollama pull <model_name>' (e.g., 'ollama pull tinyllama').")
        print("If issues persist, try uncommenting LITELLM_DEBUG in main.py for more logs.")

if __name__ == "__main__":
    run_debate()
