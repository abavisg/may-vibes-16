import os
import logging
import json
from datetime import datetime
from crewai import LLM, Agent, Crew, Process, Task
from crew.debate_crew import create_debate_crew, format_debate_results
from tasks.pro_task import pro_debate_task, pro_rebuttal_task, pro_task
from tasks.con_task import con_debate_task, con_rebuttal_task, con_task
from tasks.mod_task import mod_task
from protocol import DebateContext, DebateProtocol
from controller import DebateController, AgentTurn

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

def save_debate_history(controller):
    """Save the debate history to a file using Model Context Protocol format."""
    try:
        # Create the outputs directory if it doesn't exist
        os.makedirs("outputs", exist_ok=True)
        
        # Create a filename based on the topic and timestamp
        filename = f"outputs/debate_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        # Save the controller state to a file
        with open(filename, "w") as f:
            json.dump(controller.to_dict(), f, indent=2)
            
        logger.info(f"Saved debate history to {filename}")
        return filename
        
    except Exception as e:
        logger.error(f"Error saving debate history: {e}")
        return None

def format_debate_transcript(controller):
    """Format the debate transcript in a readable way."""
    topic = controller.topic
    max_rounds = controller.max_rounds
    
    # Prepare formatted output
    output = []
    output.append("=" * 60)
    output.append(f"DEBATE SUMMARY: {topic}")
    output.append("=" * 60)
    output.append("")
    
    # Get all messages by type
    pro_messages = controller.context.get_messages_for_side("pro")
    con_messages = controller.context.get_messages_for_side("con")
    mod_messages = controller.context.get_messages_for_agent("mia")
    
    # Format initial arguments
    if pro_messages and len(pro_messages) > 0:
        output.append("PRO INITIAL ARGUMENT")
        output.append("-" * 60)
        output.append(pro_messages[0]["content"])
        output.append("")
    
    if con_messages and len(con_messages) > 0:
        output.append("CON INITIAL ARGUMENT")
        output.append("-" * 60)
        output.append(con_messages[0]["content"])
        output.append("")
    
    # Format rebuttals
    if max_rounds > 0 and (len(pro_messages) > 1 or len(con_messages) > 1):
        output.append("REBUTTALS")
        output.append("-" * 60)
        
        for round_num in range(1, max_rounds + 1):
            # Find pro rebuttal for this round
            pro_rebuttal = next((msg for msg in pro_messages if msg.get("round") == round_num), None)
            # Find con rebuttal for this round
            con_rebuttal = next((msg for msg in con_messages if msg.get("round") == round_num), None)
            
            if pro_rebuttal or con_rebuttal:
                output.append(f"Round {round_num}:")
                
                if pro_rebuttal:
                    output.append(f"Pro: {pro_rebuttal['content']}")
                
                if con_rebuttal:
                    output.append(f"Con: {con_rebuttal['content']}")
                
                output.append("")
    
    # Format moderator evaluation
    if mod_messages:
        output.append("CONCLUSION")
        output.append("-" * 60)
        output.append(mod_messages[0]["content"])
        output.append("")
    
    # Add metadata
    output.append("-" * 60)
    output.append(f"Debate format: Initial arguments + {max_rounds} rebuttal(s) per side")
    output.append(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    output.append("=" * 60)
    
    return "\n".join(output)

def run_debate():
    """Run the main debate application using DebateController."""
    try:
        # Get debate topic from user
        debate_topic = get_user_topic()
        logger.info(f"Debate topic: {debate_topic}")
        
        # Get number of rebuttals from user
        num_rebuttals = get_num_rebuttals()
        logger.info(f"Number of rebuttals per side: {num_rebuttals}")
        
        # Create the debate controller
        controller = DebateController(topic=debate_topic, max_rounds=num_rebuttals)
        
        # Run the debate loop
        print(f"\nStarting a debate on: {debate_topic}")
        print(f"Format: Initial arguments + {num_rebuttals} rebuttal(s) per side")
        print("=" * 50)
        
        # Initialize the turn to Pro if not already set
        controller.turn = AgentTurn.PRO
        
        while True:
            # Get the current agent to act
            current_agent = controller.turn
            round_number = controller.round_number
            
            # If we're done, exit the loop
            if current_agent == AgentTurn.DONE:
                break
            
            # Get context for the agent
            context = controller.get_all_messages()
            
            # Generate response based on agent type
            if current_agent == AgentTurn.PRO:
                print(f"Round {round_number}: Pro agent (Ava) is thinking...")
                response = pro_task(context, llm=ollama_llm)
            elif current_agent == AgentTurn.CON:
                print(f"Round {round_number}: Con agent (Ben) is thinking...")
                response = con_task(context, llm=ollama_llm)
            elif current_agent == AgentTurn.MOD:
                print(f"Moderator (Mia) is evaluating the debate...")
                response = mod_task(context, llm=ollama_llm)
            
            # Add the response to the controller
            controller.add_message(response)
            
            # Print the response content
            print(f"{current_agent.value.capitalize()}: {response['content']}")
            print("-" * 50)
            
            # Advance to the next agent
            # The next_agent method handles transitioning between agents and rounds
            controller.next_agent()
        
        # Save the debate history
        save_debate_history(controller)
        
        # Format the debate transcript
        transcript = format_debate_transcript(controller)
        
        return transcript

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
        print("\nThe debate has been saved to the outputs directory using the Model Context Protocol format.")

    except Exception as e:
        logger.error(f"Application error: {e}")
        raise
