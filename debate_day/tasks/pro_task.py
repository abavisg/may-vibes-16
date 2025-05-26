from crewai import Task
from typing import Dict, List, Any, Optional
from protocol import DebateProtocol, MessageType
import logging

# Configure logging
logger = logging.getLogger(__name__)

def pro_task(messages: List[Dict[str, Any]], llm=None) -> Dict[str, Any]:
    """
    Processes recent messages and determines what Ava (Pro agent) should say next,
    using an LLM to generate the content.
    
    Args:
        messages: A list of recent debate messages
        llm: Language model instance to use for generating responses
        
    Returns:
        A formatted message using DebateProtocol
    """
    # Default values
    agent_id = "ava"
    side = "pro"
    round_number = 0
    
    # If no LLM is provided, use fallback hardcoded responses
    if llm is None:
        logger.warning("No LLM provided to pro_task, using fallback responses")
        return _fallback_pro_response(messages)
    
    # Get the topic (should be the first message)
    topic = "Should artificial intelligence be regulated by governments?"  # fallback
    for msg in messages:
        if msg.get("type") == "topic":
            topic = msg.get("content", topic)
            break
    
    # Determine the current round and what to respond to
    last_message = messages[-1] if messages else None
    
    # Find messages from Con agent to respond to
    con_messages = [msg for msg in messages if msg.get("side") == "con"]
    pro_messages = [msg for msg in messages if msg.get("side") == "pro"]
    
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
    
    # Determine the round number and prompt
    if not con_messages:
        # Initial argument (no Con messages yet)
        round_number = 0
        prompt = f"""You are Ava, an expert debater arguing IN FAVOR of the topic.
        
Topic: {topic}

Your task: Provide one clear, focused argument supporting this position. 
Be direct and concise, presenting your argument in 1-2 sentences that are compelling and evidence-based.

Your response should be a single paragraph with no introductory phrases like "I believe" or "In my opinion."
"""
    else:
        # Find the latest Con message
        latest_con = con_messages[-1]
        con_round = latest_con.get("round", 0)
        
        # Check if Pro has already responded in this round
        pro_in_current_round = any(msg.get("round") == con_round for msg in pro_messages)
        
        if pro_in_current_round:
            # Pro has already argued in this round, move to next round
            round_number = con_round + 1
            
            prompt = f"""You are Ava, an expert debater arguing IN FAVOR of the topic.

Debate History:
{history}

Topic: {topic}

Current round: {round_number}

Your task: Continue supporting your position with a new rebuttal. 
Address any weaknesses in Ben's previous argument and strengthen your original position.
Be focused and precise, offering a compelling response in 1-2 sentences maximum.

Your response should be a single paragraph with no introductory phrases like "I believe" or "In my opinion."
"""
        else:
            # Pro needs to respond in the current round
            round_number = con_round
            
            prompt = f"""You are Ava, an expert debater arguing IN FAVOR of the topic.

Debate History:
{history}

Topic: {topic}

Current round: {round_number}

Your task: Rebut Ben's counter-argument with your own follow-up point.
Your rebuttal should directly address the flaws or weaknesses in their argument.
Be focused and precise, offering a compelling response in 1-2 sentences maximum.

Your response should be a single paragraph with no introductory phrases like "I believe" or "In my opinion."
"""
    
    # Generate response using the LLM
    try:
        logger.info(f"Generating Pro response for round {round_number}")
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
        logger.error(f"Error generating Pro response: {e}")
        # Fall back to hardcoded responses on error
        return _fallback_pro_response(messages)

def _fallback_pro_response(messages: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Fallback function that returns hardcoded responses if LLM fails."""
    # Default values
    agent_id = "ava"
    side = "pro"
    round_number = 0
    
    # Get the topic (should be the first message)
    topic = "Should artificial intelligence be regulated by governments?"  # fallback
    for msg in messages:
        if msg.get("type") == "topic":
            topic = msg.get("content", topic)
            break
    
    # Determine the current round and what to respond to
    last_message = messages[-1] if messages else None
    
    if not last_message or last_message.get("type") == "topic":
        # Initial argument (no prior messages or only topic)
        if "moon" in topic.lower():
            content = "Overwhelming scientific evidence confirms the Apollo missions landed on the moon, including thousands of photos, moon rocks, and retroreflectors still used today."
        elif "ai" in topic.lower() or "artificial intelligence" in topic.lower():
            content = "AI regulation is necessary to prevent potential harms while allowing beneficial innovation."
        elif "remote work" in topic.lower():
            content = "Remote work increases productivity, eliminates commuting time, and provides flexibility that improves work-life balance."
        else:
            # Generic response for any topic
            content = f"Taking the affirmative position, I support {topic} based on evidence and logical reasoning."
        
        return DebateProtocol.argument_message(
            content=content,
            side=side,
            agent_id=agent_id,
            round_number=0
        )
    
    # Find messages from Con agent to respond to
    con_messages = [msg for msg in messages if msg.get("side") == "con"]
    if not con_messages:
        # No Con messages to respond to yet
        if "moon" in topic.lower():
            content = "Overwhelming scientific evidence confirms the Apollo missions landed on the moon, including thousands of photos, moon rocks, and retroreflectors still used today."
        elif "ai" in topic.lower() or "artificial intelligence" in topic.lower():
            content = "AI regulation is necessary to prevent potential harms while allowing beneficial innovation."
        else:
            # Generic response for any topic
            content = f"Taking the affirmative position, I support {topic} based on evidence and logical reasoning."
        
        return DebateProtocol.argument_message(
            content=content,
            side=side,
            agent_id=agent_id,
            round_number=0
        )
    
    # Determine round number based on latest Con message
    latest_con = con_messages[-1]
    con_round = latest_con.get("round", 0)
    
    # Pro rebuttal should be in the same round as Con's argument if Con just started a new round,
    # or in the next round if Pro is starting a new round
    pro_messages = [msg for msg in messages if msg.get("side") == "pro"]
    pro_in_current_round = any(msg.get("round") == con_round for msg in pro_messages)
    
    if pro_in_current_round:
        # Pro has already argued in this round, move to next round
        round_number = con_round + 1
        
        # Generate different responses for different rounds
        if "moon" in topic.lower():
            if round_number == 1:
                content = f"The Soviet Union, our rival in the Space Race, would have exposed any hoax rather than acknowledging our achievement."
            elif round_number == 2:
                content = f"Moon landing conspiracy theories neglect thousands of scientists and engineers who worked independently on the Apollo program."
            else:
                content = f"Modern satellite imagery from multiple countries has confirmed the landing sites and equipment left on the lunar surface."
        elif "ai" in topic.lower() or "artificial intelligence" in topic.lower():
            if round_number == 1:
                content = f"Industry self-regulation has proven insufficient as evidenced by multiple ethical violations in AI development."
            elif round_number == 2:
                content = f"Balanced regulation can accelerate responsible innovation by providing clear guidelines and standards."
            else:
                content = f"The potential risks of unregulated AI, including discrimination and safety concerns, outweigh the temporary innovation slowdown."
        elif "remote work" in topic.lower():
            if round_number == 1:
                content = f"Studies show remote workers report higher job satisfaction and lower turnover rates compared to office-based employees."
            elif round_number == 2:
                content = f"Companies can access global talent pools rather than being limited to local candidates when embracing remote work."
            else:
                content = f"Remote work reduces organizational costs for office space, utilities, and other facilities management expenses."
        else:
            # Generic response for any topic and round
            content = f"The opposition's point overlooks critical evidence supporting my position on {topic} in round {round_number}."
    else:
        # Pro needs to respond in the current round
        round_number = con_round
        
        # Generate different responses for different rounds
        if "moon" in topic.lower():
            if round_number == 1:
                content = f"The conspiracy would require thousands of people to maintain a secret for decades, which is statistically impossible."
            elif round_number == 2:
                content = f"The moon rocks brought back have properties that cannot be replicated on Earth and have been verified by independent scientists worldwide."
            else:
                content = f"The technology to fake the moon landing footage simply didn't exist in 1969 - film experts have conclusively demonstrated this."
        elif "ai" in topic.lower() or "artificial intelligence" in topic.lower():
            if round_number == 1:
                content = f"Effective regulation creates market certainty and encourages investment in responsible AI development."
            elif round_number == 2:
                content = f"History shows that unregulated technologies often lead to monopolistic control and reduced innovation over time."
            else:
                content = f"Many AI leaders themselves are calling for regulation to prevent misuse and establish trust with the public."
        elif "remote work" in topic.lower():
            if round_number == 1:
                content = f"Remote work significantly reduces carbon emissions by eliminating daily commutes, supporting environmental sustainability."
            elif round_number == 2:
                content = f"Modern collaboration tools effectively address communication challenges, as demonstrated during the global pandemic."
            else:
                content = f"Remote work promotes diversity and inclusion by removing geographical and physical barriers to employment."
        else:
            # Generic response for any topic
            content = f"Considering the counter-argument, the evidence still strongly supports my position on {topic}."
    
    # Create the response using DebateProtocol
    return DebateProtocol.argument_message(
        content=content,
        side=side,
        agent_id=agent_id,
        round_number=round_number
    )

# Keep the existing Task objects for compatibility with the CrewAI framework
pro_debate_task = Task(
    description=(
        "This is a debate about whether artificial intelligence should be regulated by governments. "
        "Your role is to argue IN FAVOR of government regulation of AI. "
        "Provide exactly one clear, focused argument supporting the topic: 'Should artificial intelligence be regulated by governments?'. "
        "Be direct and concise, presenting your argument in 1-2 sentences that are compelling and evidence-based."
    ),
    expected_output=(
        "A single, concise argument in favor of the topic, expressed in 1-2 sentences maximum."
    ),
    # agent is assigned in debate_crew.py
)

# Add a rebuttal task for the Pro agent to respond to the Con agent's argument
pro_rebuttal_task = Task(
    description=(
        "Review the Con agent's argument carefully. "
        "This is your opportunity to rebut their counter-argument with your own follow-up point. "
        "Your rebuttal should directly address the flaws or weaknesses in their argument. "
        "Be focused and precise, offering a compelling response that strengthens your original position. "
        "Your rebuttal should be 1-2 sentences maximum."
    ),
    expected_output=(
        "A concise, focused rebuttal that directly addresses the Con agent's argument, "
        "expressed in 1-2 sentences maximum."
    ),
    # agent is assigned in debate_crew.py
)
