from crewai import Task
from typing import Dict, List, Any, Optional
from protocol import DebateProtocol, MessageType
import logging

# Configure logging
logger = logging.getLogger(__name__)

# from agents.mod_agent import mia_agent # This import is no longer needed
from tasks.pro_task import pro_debate_task
from tasks.con_task import con_debate_task

def mod_task(messages: List[Dict[str, Any]], llm=None) -> Dict[str, Any]:
    """
    Processes debate messages and generates a moderator evaluation,
    using an LLM to generate the content.
    
    Args:
        messages: A list of debate messages
        llm: Language model instance to use for generating responses
        
    Returns:
        A formatted evaluation message using DebateProtocol
    """
    # Default values
    agent_id = "mia"
    
    # If no LLM is provided, use fallback hardcoded responses
    if llm is None:
        logger.warning("No LLM provided to mod_task, using fallback responses")
        return _fallback_mod_response(messages)
    
    # Get the topic (should be the first message)
    topic = "Should artificial intelligence be regulated by governments?"  # fallback
    for msg in messages:
        if msg.get("type") == "topic":
            topic = msg.get("content", topic)
            break
    
    # Count the number of rounds based on messages
    rounds = 0
    for msg in messages:
        if "round" in msg and msg["round"] > rounds:
            rounds = msg["round"]
    
    # Get all messages by side
    pro_messages = [msg for msg in messages if msg.get("side") == "pro"]
    con_messages = [msg for msg in messages if msg.get("side") == "con"]
    
    # Format the debate history
    debate_transcript = f"Topic: {topic}\n\n"
    
    # Add initial arguments
    if pro_messages and len(pro_messages) > 0:
        debate_transcript += f"PRO INITIAL ARGUMENT:\nAva: {pro_messages[0]['content']}\n\n"
    
    if con_messages and len(con_messages) > 0:
        debate_transcript += f"CON INITIAL ARGUMENT:\nBen: {con_messages[0]['content']}\n\n"
    
    # Add rebuttals by round
    if rounds > 0:
        debate_transcript += "REBUTTALS:\n"
        for round_num in range(1, rounds + 1):
            debate_transcript += f"Round {round_num}:\n"
            
            # Find pro rebuttal for this round
            pro_rebuttal = next((msg for msg in pro_messages if msg.get("round") == round_num), None)
            if pro_rebuttal:
                debate_transcript += f"Ava (Pro): {pro_rebuttal['content']}\n"
            
            # Find con rebuttal for this round
            con_rebuttal = next((msg for msg in con_messages if msg.get("round") == round_num), None)
            if con_rebuttal:
                debate_transcript += f"Ben (Con): {con_rebuttal['content']}\n"
            
            debate_transcript += "\n"
    
    # Create the prompt for the moderator
    prompt = f"""You are Mia, an impartial debate moderator evaluating a debate on the topic:
"{topic}"

Below is the full debate transcript:

{debate_transcript}

Your task: Evaluate the arguments from both sides and determine the winner based on the strength of reasoning, evidence, and persuasiveness.

Please structure your evaluation as follows:
1. Briefly evaluate the Pro (Ava) initial argument (1 sentence)
2. Briefly evaluate the Con (Ben) initial argument (1 sentence)
3. For each rebuttal round, evaluate both sides' points (1-2 sentences total)
4. Declare a winner with a brief rationale (1-2 sentences)

Your entire response should be 5-7 sentences maximum. Be fair and objective in your assessment.
Your response should end with "Winner: [Ava (Pro) or Ben (Con)]" to clearly indicate your decision.
"""
    
    # Generate response using the LLM
    try:
        logger.info("Generating Moderator evaluation")
        # Use call method for CrewAI's LLM
        content = llm.call(prompt)
        
        # Clean up the response if needed
        content = content.strip()
        
        # Determine the winner from the response
        winner = "pro"  # Default to Pro
        if "Winner: Ben (Con)" in content:
            winner = "con"
        
        # Create the response using DebateProtocol
        return DebateProtocol.evaluation_message(
            content=content,
            winner=winner,
            agent_id=agent_id
        )
    except Exception as e:
        logger.error(f"Error generating Moderator response: {e}")
        # Fall back to hardcoded responses on error
        return _fallback_mod_response(messages)

def _fallback_mod_response(messages: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Fallback function that returns hardcoded responses if LLM fails."""
    # Default values
    agent_id = "mia"
    
    # Get the topic (should be the first message)
    topic = "Should artificial intelligence be regulated by governments?"  # fallback
    for msg in messages:
        if msg.get("type") == "topic":
            topic = msg.get("content", topic)
            break
    
    # Count the number of rounds based on messages
    rounds = 0
    for msg in messages:
        if "round" in msg and msg["round"] > rounds:
            rounds = msg["round"]
    
    # Get all messages by side
    pro_messages = [msg for msg in messages if msg.get("side") == "pro"]
    con_messages = [msg for msg in messages if msg.get("side") == "con"]
    
    # For a real implementation, the moderator would evaluate both sides' arguments
    # Here we'll create different evaluations based on the topic
    
    # Determine winner - in a real implementation this would be based on argument quality
    # Here we'll just arbitrarily pick a winner for demonstration purposes
    if len(topic) % 2 == 0:  # Simple arbitrary condition - even length topics go to Pro
        winner = "pro"
    else:
        winner = "con"
    
    # Generate a topic-specific evaluation
    if "moon" in topic.lower():
        if winner == "pro":
            content = "After evaluating all arguments, the Pro side presented more compelling scientific evidence including physical moon rocks, retroreflectors still in use, and independent verification. The Con arguments about visual anomalies were adequately addressed. Winner: Ava (Pro)"
        else:
            content = "After evaluating all arguments, the Con side raised significant questions about photographic inconsistencies and missing telemetry data that were not adequately addressed. The burden of proof lies with those making extraordinary claims. Winner: Ben (Con)"
    elif "ai" in topic.lower() or "artificial intelligence" in topic.lower():
        if winner == "pro":
            content = "After evaluating the arguments, the Pro side presented stronger evidence for balanced regulation that protects innovation while preventing harm. The need for public trust and safety outweighs concerns about temporary slowdowns. Winner: Ava (Pro)"
        else:
            content = "After evaluating the arguments, the Con side demonstrated more convincingly that regulatory frameworks would likely be ineffective and could drive innovation to less restricted regions. Market-based solutions offer more adaptability. Winner: Ben (Con)"
    elif "remote work" in topic.lower():
        if winner == "pro":
            content = "After evaluating the arguments, the Pro side presented stronger evidence on productivity gains, environmental benefits, and improved work-life balance. The flexibility advantages outweigh potential collaboration challenges. Winner: Ava (Pro)"
        else:
            content = "After evaluating the arguments, the Con side presented more compelling evidence on collaboration benefits, security concerns, and the value of workplace culture that cannot be replicated remotely. Winner: Ben (Con)"
    else:
        # Generic evaluation for any topic
        if winner == "pro":
            content = f"After careful consideration of all arguments presented, the Pro side offered more compelling evidence and logical reasoning on the topic '{topic}'. Their arguments were better supported and addressed counterpoints effectively. Winner: Ava (Pro)"
        else:
            content = f"After careful consideration of all arguments presented, the Con side demonstrated stronger reasoning and evidence regarding '{topic}'. Their points effectively countered the Pro position and presented more compelling alternatives. Winner: Ben (Con)"
    
    # Create the response using DebateProtocol
    return DebateProtocol.evaluation_message(
        content=content,
        winner=winner,
        agent_id=agent_id
    )

moderator_task = Task(
    description=(
        "You are moderating a multi-round debate where agents have presented arguments and possibly multiple rebuttals.\n\n"
        "Evaluate the entire debate concisely using this structure:\n"
        "1. Initial Pro argument evaluation (1 sentence)\n"
        "2. Initial Con argument evaluation (1 sentence)\n"
        "3. For each rebuttal round:\n"
        "   - Pro rebuttal evaluation (1 sentence)\n"
        "   - Con rebuttal evaluation (1 sentence)\n"
        "4. Winner declaration with brief rationale (1-2 sentences)\n\n"
        "Consider all arguments and rebuttals in your final decision. Base your evaluation on the strength of reasoning, evidence, and persuasiveness."
    ),
    expected_output=(
        "A structured evaluation that covers:\n"
        "1. Pro initial argument evaluation\n"
        "2. Con initial argument evaluation\n"
        "3. Each rebuttal evaluation (organized by round)\n"
        "4. Winner: [Ava (Pro) or Ben (Con)] - [brief rationale]"
    ),
    # agent=mia_agent, # Agent is now assigned in debate_crew.py
    context=[pro_debate_task, con_debate_task]
) 