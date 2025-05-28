# Debate Day

A command-line application that simulates a debate between AI agents using local LLM models, with two distinct architecture options.

## Features

- Debate between Pro and Con AI agents on any topic
- Configurable number of rebuttals (0-3)
- Impartial moderator evaluation with declared winner
- Uses local Ollama models for generating dynamic AI-driven content
- Fallback to hardcoded responses if LLM is unavailable
- Saves debate history to outputs directory
- MCP server for centralized debate management
- Autonomous agent architecture with modular design
- CLI tools for orchestrating debates
- Real-time debate viewer for monitoring debate progress

## Architectures

The system offers two different architectures:

### 1. CrewAI-Based Architecture (Legacy)

The original implementation uses the CrewAI framework:

- **Controller**: Manages debate flow, turns, rounds, and context
- **Tasks**: Generate content for each agent (Pro, Con, Moderator)
- **Crew**: Coordinates agents using the CrewAI framework
- **LLM Integration**: Uses CrewAI's LLM class to connect with local Ollama models

To use this version, run:
```
python debate_day/main.py
```

### 2. Autonomous Agent Architecture (Current)

The newer implementation uses standalone agents that communicate via the MCP server:

- **MCP Server**: FastAPI-based central server for debate management
- **Protocol**: Defines message formats and standardizes communication
- **Agent Modules**: Self-contained agent implementations in dedicated directories
- **CLI Tools**: Utilities for starting debates and managing agents

To use this version, run:
```
python cli_tools/run_debate.py
```

## Requirements

- Python 3.9+
- Ollama (running locally with llama3 model)
- FastAPI and uvicorn (for MCP server)
- httpx for HTTP requests
- loguru for logging

## Installation

1. Clone the repository
2. Install the package in development mode:
   ```
   pip install -e .
   ```
3. Install additional dependencies:
   ```
   pip install httpx loguru
   ```
4. Make sure Ollama is running locally with the llama3 model:
   ```
   ollama run llama3
   ```

## Usage

### Quickstart (Recommended)

Run a complete debate with a single command:

```
python cli_tools/run_debate.py
```

This all-in-one script handles everything:
1. Starts the MCP server
2. Creates a new debate
3. Launches all agents
4. Monitors all processes

You can customize the topic, number of rounds, and agent names:

```
python cli_tools/run_debate.py --topic "Democracy is the best form of government" --rounds 2 --pro-name Alice --con-name Bob
```

### View a Running Debate

You can watch the progress of a debate in real-time using the debate viewer:

```
python cli_tools/view_debate.py --debate-id YOUR_DEBATE_ID
```

This will display the debate messages with color-coding for each participant and automatically refresh as new messages arrive. Options include:

- `--clear`: Clear the terminal between updates for a cleaner display
- `--refresh 1.0`: Set the refresh interval in seconds (default: 2.0)
- `--mcp-url`: Specify a custom MCP server URL if not using the default

The viewer will show:
- Current debate status and round information
- Who is speaking next
- All debate messages organized by round
- Final verdict and winner when the debate concludes

### Run the Legacy CLI Application

Run the original command-line application:

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

### Start a Debate with CLI Tools

Use the debate bootstrapper to start a new debate and optionally launch all agents:

```
python cli_tools/start_debate.py --topic "Artificial intelligence will ultimately benefit humanity" --rounds 2 --launch-agents
```

For more options and examples, see the [CLI Tools documentation](cli_tools/README.md).

### Launch Agents for an Existing Debate

If you've already started a debate but need to launch or relaunch agents:

```
python cli_tools/launch_agents.py --debate-id your-debate-id
```

You can also launch a specific agent:

```
python cli_tools/launch_agents.py --debate-id your-debate-id --role pro
```

For more options and examples, see the [CLI Tools documentation](cli_tools/README.md).

## API Endpoints

The MCP server provides the following endpoints:

- `POST /api/start` - Start a new debate
- `POST /api/message/{debate_id}` - Add a message to a debate
- `GET /api/context/{debate_id}` - Get message history
- `GET /api/turn/{debate_id}` - Get turn information
- `GET /api/status/{debate_id}` - Get debate status
- `GET /api/debates` - List all debates
- `GET /api/debate/{debate_id}` - Get detailed debate information

## Agent Modules

The system includes three specialized agent modules:

- **Pro Agent**: Argues in favor of the debate topic
- **Con Agent**: Argues against the debate topic
- **Moderator Agent**: Evaluates arguments and declares a winner

Each agent is implemented as a standalone module in the `debate_day/agents` directory with its own configuration and strategy.

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

The system uses Ollama for generating dynamic, contextual responses. Each agent connects to Ollama independently and provides fallback responses if the LLM is unavailable.

Key features of the LLM integration:
- Context-aware prompts that include debate history
- Round-specific prompt engineering for each agent
- Fallback mechanism to ensure robustness
- Clean-up of LLM responses to match debate format 