# Con Agent for Debate Day 2.0

This agent represents the CON side in Debate Day debates, automatically participating by communicating with the MCP server.

## Features

- Automatic polling of MCP server to determine when it's the agent's turn
- Fetches debate context and builds appropriate prompts based on debate state
- Uses Ollama to generate responses with the specified LLM
- Handles message posting and turn management
- Comprehensive logging
- Critical and rebuttal-focused strategy

## Configuration

All configuration is done through the `.env` file:

```
ROLE=con                            # The agent's role (should be "con")
MODEL=llama3                        # The Ollama model to use
MCP_SERVER_URL=http://localhost:8000 # URL of the MCP server
AGENT_NAME=Ben                      # The agent's name
DEBATE_ID=test-debate-id-001        # ID of the debate to participate in
```

## Requirements

- Python 3.9+
- Ollama running locally with the specified model
- MCP server running at the specified URL

## Installation

1. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Make sure Ollama is running with the specified model:
   ```
   ollama run llama3
   ```

## Usage

Run the agent:

```
python main.py
```

The agent will automatically:
1. Check if it's its turn to speak
2. Fetch the debate context
3. Generate a response
4. Post the message to the MCP server

## Strategy

The agent uses different prompting strategies based on the debate round:

- **Round 0**: Initial counter-argument establishing a strong critical stance
- **Later rounds**: Targeted rebuttals that directly address the Pro's points, pointing out logical fallacies, missing evidence, or flawed assumptions

The `strategy.py` module is specifically designed to create a critical and incisive debate style that effectively counters the PRO side's arguments. 