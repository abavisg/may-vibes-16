from crew.debate_crew import create_debate_crew
import os

# --- LLM Configuration for Ollama ---
# Set this flag to True to use the higher quality model (e.g., llama3),
# or False to use a faster model for development (e.g., tinyllama).
USE_HIGH_QUALITY_MODEL = False  # True for llama3, False for tinyllama

OLLAMA_API_BASE = 'http://localhost:11434/v1'

if USE_HIGH_QUALITY_MODEL:
    OLLAMA_MODEL_NAME = 'llama3' 
    print(f"Using high-quality Ollama model: {OLLAMA_MODEL_NAME}")
else:
    OLLAMA_MODEL_NAME = 'tinyllama'
    print(f"Using development Ollama model: {OLLAMA_MODEL_NAME}")

# Set environment variables for CrewAI to use Ollama
os.environ["OPENAI_API_BASE"] = OLLAMA_API_BASE
os.environ["OPENAI_MODEL_NAME"] = OLLAMA_MODEL_NAME
os.environ["OPENAI_API_KEY"] = 'ollama'  # Required by CrewAI, can be any non-empty string for Ollama
# ---

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

    # Create the debate crew
    debate_squad = create_debate_crew(topic)

    print("\nKicking off the debate...\n")
    # The verbose output from the crew (set to 2) will print the turn-by-turn debate.
    # The result variable will hold the output of the final task.
    try:
        result = debate_squad.kickoff()

        print("\n------------------------------------")
        print("🏁 Debate Concluded! 🏁")
        print("------------------------------------\n")
        print("Final Output (Moderator's Assessment):\n")
        print(result)
    except Exception as e:
        print(f"\nAn error occurred during the debate: {e}")
        print("\nPlease ensure your Ollama server is running and the specified model is available.")
        print(f"Attempted to use model: {OLLAMA_MODEL_NAME} via {OLLAMA_API_BASE}")
        print("You can pull models using 'ollama pull <model_name>' (e.g., 'ollama pull tinyllama').")

if __name__ == "__main__":
    run_debate()
