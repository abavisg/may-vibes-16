# Debate Day

A command-line application that simulates a debate between AI agents using the CrewAI framework and local LLM models.

## Features

- Debate between Pro and Con AI agents on any topic
- Configurable number of rebuttals (0-3)
- Impartial moderator evaluation with declared winner
- Uses local Ollama models for generating dynamic AI-driven content
- Fallback to hardcoded responses if LLM is unavailable
- Saves debate history to outputs directory
- MCP server for centralized debate management

## Architecture

The system uses a controller-driven architecture with clear separation of concerns:

- **Controller**: Manages debate flow, turns, rounds, and context
- **Protocol**: Defines message formats and standardizes communication
- **Tasks**: Generate content for each agent (Pro, Con, Moderator)
- **LLM Integration**: Uses CrewAI's LLM class to connect with local Ollama models
- **MCP Server**: FastAPI-based central server for debate management

## Requirements

- Python 3.9+
- CrewAI library
- Ollama (running locally with llama3 model)
- FastAPI and uvicorn (for MCP server)

## Installation

1. Clone the repository
2. Install the package in development mode:
   ```
   pip install -e .
   ```
3. Make sure Ollama is running locally with the llama3 model:
   ```
   ollama run llama3
   ```

## Usage

### Run the CLI Application

Run the command-line application:

```
python debate_day/main.py
```

Follow the prompts to:
1. Enter a debate topic (or use the default)
2. Select the number of rebuttals (0-3)

The debate will run automatically, and the results will be saved to the `outputs` directory.

### Run the MCP Server

The MCP (Model Context Protocol) server provides a central communication hub for the debate system:

```
cd debate_day
python run_mcp_server.py
```

This will start the server on http://localhost:8000. You can access the API documentation at http://localhost:8000/docs.

## API Endpoints

The MCP server provides the following endpoints:

- `POST /api/start` - Start a new debate
- `POST /api/message/{debate_id}` - Add a message to a debate
- `GET /api/context/{debate_id}` - Get message history
- `GET /api/turn/{debate_id}` - Get turn information
- `GET /api/status/{debate_id}` - Get debate status
- `GET /api/debates` - List all debates
- `GET /api/debate/{debate_id}` - Get detailed debate information

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