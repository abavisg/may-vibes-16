"""
LLM Configuration for the Pro Agent.

This module handles the integration with language models via Ollama,
providing functions to generate responses based on prompts.
"""

import os
import json
import httpx
from typing import Dict, Any, Optional
from pathlib import Path
from dotenv import load_dotenv
from loguru import logger
import traceback

# Load environment variables
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

# Configuration
MODEL = os.getenv("MODEL", "llama3")
OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://localhost:11434/api/generate")

# Model parameters
DEFAULT_PARAMS = {
    "temperature": 0.7,
    "top_p": 0.9,
    "max_tokens": 800,
    "stop": ["</response>"]
}


def generate_response(prompt: str, params: Optional[Dict[str, Any]] = None) -> str:
    """
    Generate a response from the LLM using Ollama.
    
    Args:
        prompt: The prompt to send to the model
        params: Optional parameters to override defaults
        
    Returns:
        The generated response text
    """
    # Start with default parameters
    request_params = DEFAULT_PARAMS.copy()
    
    # Override with any provided parameters
    if params:
        request_params.update(params)
    
    # Prepare the request payload
    payload = {
        "model": MODEL,
        "prompt": prompt,
        **request_params
    }
    
    logger.debug(f"Sending request to Ollama: model={MODEL}, prompt_length={len(prompt)}")
    
    try:
        # Make the API request
        response = httpx.post(
            OLLAMA_API_URL,
            json=payload,
            timeout=60.0  # Longer timeout for model inference
        )
        response.raise_for_status()
        
        # Process the streaming response
        generated_text = ""
        final_response_data = {}
        for line in response.iter_lines():
            if line:
                try:
                    chunk = json.loads(line)
                    generated_text += chunk.get("response", "")
                    # The last chunk usually contains the full context and stats
                    if chunk.get("done", False): # Ollama typically uses "done: true" in the last chunk
                        final_response_data = chunk
                except json.JSONDecodeError:
                    logger.warning(f"Failed to decode JSON line: {line}")
        
        # Log generation stats if available from the final chunk
        if "eval_count" in final_response_data:
            logger.debug(f"Generated {final_response_data.get('eval_count')} tokens in {final_response_data.get('eval_duration', 0) / 1e9:.2f}s (Total)")
        elif not generated_text: # If no text was generated and no stats, it's an issue.
             logger.warning("Ollama response was empty or not in expected format.")
             return "Error: Received an empty or invalid response from Ollama."

        if not generated_text.strip() and not final_response_data:
            logger.warning("Ollama produced an empty response string.")
            # Consider what to return here. Maybe an empty string is valid, or maybe it's an error.
            # For now, returning the empty string as it might be a valid (though unusual) model output.

        return generated_text.strip()
    
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error from Ollama: {e.response.status_code} - {e.response.text}")
        return "Error: Unable to generate a response due to an API error."
    
    except httpx.RequestError as e:
        logger.error(f"Request error: {e}")
        return "Error: Unable to connect to Ollama. Please ensure the service is running."
    
    except Exception as e:
        logger.error(f"Unexpected error: {e}\\n{traceback.format_exc()}")
        return "Error: An unexpected error occurred while generating a response."


def is_ollama_available() -> bool:
    """
    Check if Ollama is available and the model is ready.
    
    Returns:
        True if Ollama is available, False otherwise
    """
    try:
        # Check if Ollama is available
        response = httpx.get("http://localhost:11434/api/tags")
        response.raise_for_status()
        
        # Check if our model is available
        tags = response.json().get("models", [])
        model_names = [tag.get("name") for tag in tags]
        
        if MODEL in model_names:
            logger.info(f"Ollama is available with model {MODEL}")
            return True
        else:
            logger.warning(f"Model {MODEL} not found in Ollama. Available models: {', '.join(model_names)}")
            return False
    
    except Exception as e:
        logger.error(f"Error checking Ollama availability: {e}")
        return False 