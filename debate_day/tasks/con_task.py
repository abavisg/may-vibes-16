from crewai import Task
from typing import Dict, List, Any, Optional
from protocol import DebateProtocol, MessageType
import logging

# Configure logging
logger = logging.getLogger(__name__)

# from agents.con_agent import ben_agent # This import is no longer needed
from tasks.pro_task import pro_debate_task # To access the context from pro_debate_task

def con_task(messages: List[Dict[str, Any]], llm=None) -> Dict[str, Any]:
    """
    Processes recent messages and determines what Ben (Con agent) should say next,
    using an LLM to generate the content.
    
    Args:
        messages: A list of recent debate messages
        llm: Language model instance to use for generating responses
        
    Returns:
        A formatted message using DebateProtocol
    """
    # Default values
    agent_id = "ben"
    side = "con"
    round_number = 0
    
    # If no LLM is provided, use fallback hardcoded responses
    if llm is None:
        logger.warning("No LLM provided to con_task, using fallback responses")
        return _fallback_con_response(messages)
    
    # Get the topic (should be the first message)
    topic = "Should artificial intelligence be regulated by governments?"  # fallback
    for msg in messages:
        if msg.get("type") == "topic":
            topic = msg.get("content", topic)
            break
    
    # Find messages from Pro agent to respond to
    pro_messages = [msg for msg in messages if msg.get("side") == "pro"]
    con_messages = [msg for msg in messages if msg.get("side") == "con"]
    
    # We need to find a Pro argument to respond to
    if not pro_messages:
        # No Pro messages to respond to yet - this shouldn't happen in normal flow
        logger.warning("No Pro messages found to respond to in con_task")
        return _fallback_con_response(messages)
    
    # Format debate history for context
    history = ""
    if len(messages) > 1:  # Skip just the topic message
        # Format the last few messages (up to 5) for context
        context_messages = messages[-5:] if len(messages) > 5 else messages
        for msg in context_messages:
            if msg.get("type") == "topic":
                history += f"Topic: {msg['content']}\n\n"
            elif "agent_id" in msg and "content" in msg:
                agent_name = "Ava (Pro)" if msg.get("agent_id") == "ava" else "Ben (Con)" if msg.get("agent_id") == "ben" else "Moderator"
                history += f"{agent_name}: {msg['content']}\n\n"
    
    # Find the latest Pro message
    latest_pro = pro_messages[-1]
    pro_round = latest_pro.get("round", 0)
    
    # Con should respond in the same round as Pro's latest message
    round_number = pro_round
    
    # Check if Con has already responded in this round
    con_in_current_round = any(msg.get("round") == pro_round for msg in con_messages)
    
    # Determine the appropriate prompt based on the round
    if con_in_current_round:
        # Con has already argued in this round, unusual flow
        round_number = pro_round + 1
        prompt = f"""You are Ben, an expert debater arguing AGAINST the topic.

Debate History:
{history}

Topic: {topic}

Current round: {round_number}

Your task: Continue opposing the topic with a new argument.
Present a clear, focused counter-argument that undermines the Pro position.
Be focused and precise, offering a compelling response in 1-2 sentences maximum.

Your response should be a single paragraph with no introductory phrases like "I believe" or "In my opinion."
"""
    else:
        # Normal flow - Con responds to Pro's latest message
        if pro_round == 0:
            # Responding to initial Pro argument
            prompt = f"""You are Ben, an expert debater arguing AGAINST the topic.

Debate History:
{history}

Topic: {topic}

Your task: Review Ava's initial argument and provide a clear, focused counter-argument.
Your counter-argument should directly address and oppose Ava's position.
Be concise and specific, explaining why Ava's viewpoint is flawed or incomplete.
Your response should be 1-2 sentences long and present a compelling opposing perspective.

Your response should be a single paragraph with no introductory phrases like "I believe" or "In my opinion."
"""
        else:
            # Responding to Pro rebuttal
            prompt = f"""You are Ben, an expert debater arguing AGAINST the topic.

Debate History:
{history}

Topic: {topic}

Current round: {round_number}

Your task: Counter Ava's latest rebuttal with your own follow-up point.
Your counter-rebuttal should address the weaknesses in Ava's argument and reinforce your original position.
Be focused and precise, delivering your strongest point in a compelling way.
Your response should be 1-2 sentences maximum.

Your response should be a single paragraph with no introductory phrases like "I believe" or "In my opinion."
"""
    
    # Generate response using the LLM
    try:
        logger.info(f"Generating Con response for round {round_number}")
        # Use call method for CrewAI's LLM
        content = llm.call(prompt)
        
        # Clean up the response if needed
        content = content.strip()
        
        # Remove any common LLM prefixes
        for prefix in ["I believe that ", "In my opinion, ", "I think ", "I would argue that "]:
            if content.startswith(prefix):
                content = content[len(prefix):]
        
        # Create the response using DebateProtocol
        return DebateProtocol.argument_message(
            content=content,
            side=side,
            agent_id=agent_id,
            round_number=round_number
        )
    except Exception as e:
        logger.error(f"Error generating Con response: {e}")
        # Fall back to hardcoded responses on error
        return _fallback_con_response(messages)

def _fallback_con_response(messages: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Fallback function that returns hardcoded responses if LLM fails."""
    # Just use the original con_task implementation here
    agent_id = "ben"
    side = "con"
    round_number = 0
    
    topic = "Should artificial intelligence be regulated by governments?"  # fallback
    for msg in messages:
        if msg.get("type") == "topic":
            topic = msg.get("content", topic)
            break
    
    pro_messages = [msg for msg in messages if msg.get("side") == "pro"]
    if not pro_messages:
        if "moon" in topic.lower():
            content = "The supposed moon landing has numerous unexplained anomalies like waving flags and inconsistent shadows that suggest studio production."
        elif "ai" in topic.lower() or "artificial intelligence" in topic.lower():
            content = "Government regulation would stifle innovation and create bureaucratic obstacles to progress."
        elif "remote work" in topic.lower():
            content = "Remote work reduces team cohesion, hampers spontaneous collaboration, and blurs the boundary between work and personal life."
        else:
            content = f"Taking the opposing position, I reject {topic} based on clear contradictory evidence."
        
        return DebateProtocol.argument_message(
            content=content, 
            side=side, 
            agent_id=agent_id, 
            round_number=0
        )
    
    latest_pro = pro_messages[-1]
    pro_round = latest_pro.get("round", 0)
    round_number = pro_round
    
    con_messages = [msg for msg in messages if msg.get("side") == "con"]
    con_in_current_round = any(msg.get("round") == pro_round for msg in con_messages)
    
    if con_in_current_round:
        round_number = pro_round + 1
        if "ai" in topic.lower():
            content = f"Regulatory frameworks are often outdated before implementation due to the rapid pace of AI advancement."
        elif "moon" in topic.lower():
            content = f"NASA has allegedly lost or destroyed many original recordings and telemetry data, which raises questions about what they're hiding."
        elif "remote work" in topic.lower():
            content = f"Remote work creates inequalities between roles that can be performed remotely and those that require physical presence."
        else:
            content = f"The evidence presented by the opposition fails to address fundamental flaws in their position on {topic}."
    else:
        if pro_round == 0:
            if "moon" in topic.lower():
                content = "The supposed moon landing has numerous unexplained anomalies like waving flags and inconsistent shadows that suggest studio production."
            elif "ai" in topic.lower():
                content = "Government regulation would stifle innovation and create bureaucratic obstacles to progress."
            elif "remote work" in topic.lower():
                content = "Remote work reduces team cohesion, hampers spontaneous collaboration, and blurs the boundary between work and personal life."
            else:
                content = f"The affirmative position on {topic} ignores significant counterevidence and logical fallacies."
        else:
            if "ai" in topic.lower():
                content = f"Market-driven solutions can more efficiently address ethical concerns while maintaining innovation momentum."
            elif "moon" in topic.lower():
                content = f"The lack of stars in lunar photographs contradicts astronomical expectations for space photography without atmospheric interference."
            elif "remote work" in topic.lower():
                content = f"Studies show that creative problem-solving and innovation are enhanced by physical proximity and face-to-face interaction."
            else:
                content = f"The latest argument fails to address the fundamental problems with {topic} that I've previously identified."
    
    return DebateProtocol.argument_message(
        content=content,
        side=side,
        agent_id=agent_id,
        round_number=round_number
    )

# The topic is implicitly taken from the context of pro_debate_task

con_debate_task = Task(
    description=(
        "This is a debate about whether artificial intelligence should be regulated by governments. "
        "Your role is to argue AGAINST government regulation of AI. "
        "Review the Pro agent's argument carefully and then provide exactly one clear, focused counter-argument. "
        "Your counter-argument should directly address and oppose the Pro agent's position. "
        "Be concise and specific, explaining why the Pro agent's viewpoint is flawed or incomplete. "
        "Your response should be 1-2 sentences long and present a compelling opposing perspective."
    ),
    expected_output=(
        "A single, concise counter-argument that directly addresses and opposes the Pro agent's point, "
        "expressed in 1-2 sentences maximum."
    ),
    # agent=ben_agent, # Agent is now assigned in debate_crew.py
    context=[pro_debate_task]
)

# Add a rebuttal task for the Con agent to respond to the Pro agent's rebuttal
con_rebuttal_task = Task(
    description=(
        "Review the Pro agent's rebuttal to your initial argument. "
        "This is your final opportunity to strengthen your position with a targeted counter-rebuttal. "
        "Your counter-rebuttal should address the weaknesses in the Pro agent's rebuttal and "
        "reinforce your original argument against the topic. "
        "Be focused and precise, delivering your strongest point in a compelling way. "
        "Your counter-rebuttal should be 1-2 sentences maximum."
    ),
    expected_output=(
        "A concise, focused counter-rebuttal that directly addresses the Pro agent's rebuttal, "
        "expressed in 1-2 sentences maximum."
    ),
    # agent is assigned in debate_crew.py
)
