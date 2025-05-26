import os
import logging
from crewai import LLM, Agent, Crew, Process, Task
from crew.debate_crew import create_debate_crew
from tasks.pro_task import pro_debate_task, pro_rebuttal_task
from tasks.con_task import con_debate_task, con_rebuttal_task

# --- Basic Logging Setup ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- Disable noisy loggers ---
for logger_name in ['httpx', 'httpcore']:
    logging.getLogger(logger_name).setLevel(logging.WARNING)

# --- LLM Configuration for Ollama --- 
OLLAMA_BASE_URL = 'http://localhost:11434'
MODEL_NAME = 'llama3'

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

def get_num_rebuttals():
    """Prompt the user for the number of rebuttals each side should have."""
    print("\nHow many rebuttals should each side have?")
    print("0 = Basic debate (one argument each + moderator)")
    print("1 = Standard debate (arguments + one rebuttal each + moderator)")
    print("2 = Extended debate (arguments + two rebuttals each + moderator)")
    print("3 = Full debate (arguments + three rebuttals each + moderator)")
    
    while True:
        try:
            rebuttals = input("\nNumber of rebuttals [0-3]: ").strip()
            
            # Default to 1 rebuttal if empty
            if not rebuttals:
                return 1
                
            rebuttals = int(rebuttals)
            if 0 <= rebuttals <= 3:
                return rebuttals
            else:
                print("Please enter a number between 0 and 3.")
        except ValueError:
            print("Please enter a valid number.")

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
    
    # Update Pro rebuttal task description
    pro_rebuttal_task.description = (
        f"This is a debate about {topic}. "
        f"Review the Con agent's argument carefully. "
        f"This is your opportunity to rebut their counter-argument with your own follow-up point. "
        f"Your rebuttal should directly address the flaws or weaknesses in their argument. "
        f"Be focused and precise, offering a compelling response that strengthens your original position. "
        f"Your rebuttal should be 1-2 sentences maximum."
    )
    
    # Update Con rebuttal task description
    con_rebuttal_task.description = (
        f"This is a debate about {topic}. "
        f"Review the Pro agent's rebuttal to your initial argument. "
        f"This is your opportunity to strengthen your position with a targeted counter-rebuttal. "
        f"Your counter-rebuttal should address the weaknesses in the Pro agent's rebuttal and "
        f"reinforce your original argument against the topic. "
        f"Be focused and precise, delivering your strongest point in a compelling way. "
        f"Your counter-rebuttal should be 1-2 sentences maximum."
    )

def run_debate():
    """Run the main debate application."""
    try:
        # Get debate topic from user
        debate_topic = get_user_topic()
        logger.info(f"Debate topic: {debate_topic}")
        
        # Get number of rebuttals from user
        num_rebuttals = get_num_rebuttals()
        logger.info(f"Number of rebuttals per side: {num_rebuttals}")
        
        # Calculate total turns (initial arguments + rebuttals)
        total_turns = num_rebuttals + 1
        
        # Update task descriptions with the user-provided topic
        update_task_descriptions(debate_topic)
        
        # Create the debate crew with our configured LLM
        crew = create_debate_crew(llm=ollama_llm, num_rebuttals=num_rebuttals)

        # Run the debate
        print(f"\nStarting a debate on: {debate_topic}")
        print(f"Format: Initial arguments + {num_rebuttals} rebuttal(s) per side")
        print("=" * 50)
        result = crew.kickoff()
        return result

    except Exception as e:
        logger.error(f"Error running debate: {e}")
        raise

if __name__ == "__main__":
    try:
        # Run the actual debate
        print("Starting debate application...")
        debate_result = run_debate()
        print("\nDebate Result:")
        print(debate_result)

    except Exception as e:
        logger.error(f"Application error: {e}")
        raise
