# Pro Agent for Debate Day 2.0

This agent represents the PRO side in Debate Day debates, automatically participating by communicating with the MCP server.

## Features

- Automatic polling of MCP server to determine when it's the agent's turn
- Fetches debate context and builds appropriate prompts based on debate state
- Uses Ollama to generate responses with the specified LLM
- Handles message posting and turn management
- Comprehensive logging

## Configuration

All configuration is done through the `.env` file:

```
ROLE=pro                            # The agent's role (should be "pro")
MODEL=llama3                        # The Ollama model to use
MCP_SERVER_URL=http://localhost:8000 # URL of the MCP server
AGENT_NAME=Ava                      # The agent's name
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

- **Round 0**: Initial argument focusing on strong points in favor of the topic
- **Later rounds**: Rebuttals that address the opponent's points while reinforcing the PRO position

The `strategy.py` module handles prompt creation and response parsing, ensuring responses are appropriate for the debate format. 