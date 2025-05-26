# Debate Day

A command-line application that simulates a debate between AI agents using the CrewAI framework and local LLM models.

## Features

- Debate between Pro and Con AI agents on any topic
- Configurable number of rebuttals (0-3)
- Impartial moderator evaluation with declared winner
- Uses local Ollama models for generating dynamic AI-driven content
- Fallback to hardcoded responses if LLM is unavailable
- Saves debate history to outputs directory

## Architecture

The system uses a controller-driven architecture with clear separation of concerns:

- **Controller**: Manages debate flow, turns, rounds, and context
- **Protocol**: Defines message formats and standardizes communication
- **Tasks**: Generate content for each agent (Pro, Con, Moderator)
- **LLM Integration**: Uses CrewAI's LLM class to connect with local Ollama models

## Requirements

- Python 3.9+
- CrewAI library
- Ollama (running locally with llama3 model)

## Installation

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Make sure Ollama is running locally with the llama3 model:
   ```
   ollama run llama3
   ```

## Usage

Run the application:

```
python debate_day/main.py
```

Follow the prompts to:
1. Enter a debate topic (or use the default)
2. Select the number of rebuttals (0-3)

The debate will run automatically, and the results will be saved to the `outputs` directory.

## Sample Topics

- Did we ever go to the moon?
- Should artificial intelligence be regulated by governments?
- Is remote work better than office work?

## Output Format

The debate output follows a structured format:
- Initial arguments from both sides
- Rebuttals organized by round
- Moderator evaluation and winner declaration

## LLM Integration

The system now uses CrewAI's LLM class to connect with local Ollama models for generating dynamic, contextual responses. Each task (pro_task, con_task, mod_task) uses the LLM to generate content based on the debate context and provides fallback responses if the LLM is unavailable.

Key features of the LLM integration:
- Context-aware prompts that include debate history
- Round-specific prompt engineering for each agent
- Fallback mechanism to ensure robustness
- Clean-up of LLM responses to match debate format 