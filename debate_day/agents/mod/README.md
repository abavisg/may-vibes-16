# Moderator Agent for Debate Day 2.0

This agent serves as the MODERATOR in Debate Day debates, automatically participating by communicating with the MCP server and providing the final verdict.

## Features

- Automatic polling of MCP server to determine when it's the agent's turn
- Fetches complete debate context for comprehensive evaluation
- Uses Ollama to generate thoughtful, fair verdicts
- Extracts winner information from verdicts for debate records
- Comprehensive logging
- Declares clear winners with justification

## Configuration

All configuration is done through the `.env` file:

```
ROLE=mod                            # The agent's role (should be "mod")
MODEL=llama3                        # The Ollama model to use
MCP_SERVER_URL=http://localhost:8000 # URL of the MCP server
AGENT_NAME=Mia                      # The agent's name
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
1. Check if it's its turn to speak (after all rounds are complete)
2. Fetch the complete debate context
3. Generate a verdict that assesses both sides' arguments
4. Explicitly declare a winner
5. Post the verdict with winner metadata to the MCP server

## Strategy

The moderator agent:

- Evaluates arguments based on strength, coherence, evidence, and persuasiveness
- Ensures fair and impartial assessment of both sides
- Always declares an explicit winner in its verdict
- Provides justification for its decision

The `strategy.py` module creates prompts that encourage thorough analysis and clear verdict statements, ensuring the debate reaches a conclusive end. 