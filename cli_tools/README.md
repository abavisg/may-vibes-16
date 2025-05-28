# Debate Day CLI Tools

This directory contains command-line tools for the Debate Day system.

## start_debate.py

The `start_debate.py` script initializes a new debate via the MCP server and optionally launches the pro, con, and moderator agents as subprocesses.

### Prerequisites

- MCP server running (see `debate_day/run_mcp_server.py`)
- Ollama running locally (if launching agents)
- Required Python packages:
  ```
  httpx
  ```

### Usage

```bash
python cli_tools/start_debate.py --topic "Artificial intelligence will ultimately benefit humanity" --rounds 2 --launch-agents
```

### Command-line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--topic` | The debate topic/resolution (required) | - |
| `--rounds` | Number of debate rounds | 1 |
| `--debate-id` / `--debate_id` | Custom debate ID | Auto-generated UUID |
| `--launch-agents` | Launch pro, con, and mod agents | False |
| `--model` | Model to use for all agents | llama3 |
| `--mcp-url` | URL of the MCP server | http://localhost:8000 |
| `--agent-dir` | Directory containing agent code | debate_day/agents |
| `--pro-name` / `--pro_name` | Name for the Pro agent | Alex |
| `--con-name` / `--con_name` | Name for the Con agent | Ben |
| `--mod-name` / `--mod_name` | Name for the Moderator agent | Mia |

### Examples

1. Start a debate with 3 rounds (without launching agents):
   ```bash
   python cli_tools/start_debate.py --topic "Social media is harmful to society" --rounds 3
   ```

2. Start a debate with a custom ID and launch agents:
   ```bash
   python cli_tools/start_debate.py --topic "Democracy is the best form of government" --debate-id custom-debate-123 --launch-agents
   ```

3. Use a different LLM model:
   ```bash
   python cli_tools/start_debate.py --topic "Climate change requires immediate action" --launch-agents --model mistral
   ```

4. Customize agent names:
   ```bash
   python cli_tools/start_debate.py --topic "The internet has improved society" --pro-name Alice --con-name Bob --mod-name Charlie --launch-agents
   ```

### What it Does

1. Posts to `/api/start` on the MCP server to initialize a debate
2. If `--launch-agents` is specified:
   - Creates/overwrites `.env` files in each agent directory
   - Launches each agent as a subprocess
   - Monitors and displays agent output
   - Handles graceful termination on Ctrl+C

### Debugging Tips

If agents fail to start:
1. Check that the MCP server is running at the specified URL
2. Verify that Ollama is running with the specified model
3. Ensure agent directories exist at the specified path
4. Check agent logs for specific errors 