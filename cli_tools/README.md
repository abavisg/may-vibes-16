# Debate Day CLI Tools

This directory contains command-line tools for the Debate Day system.

## run_debate.py

The `run_debate.py` script is an all-in-one solution that handles the entire debate workflow in a single command:

1. Starts the MCP server
2. Creates a new debate
3. Launches all agent processes

This is the easiest way to run a complete debate.

### Usage

```bash
python cli_tools/run_debate.py
```

### Command-line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--topic` | The debate topic/resolution | "Is AI beneficial for humanity?" |
| `--rounds` | Number of debate rounds | 1 |
| `--debate-id` / `--debate_id` | Custom debate ID | Auto-generated UUID |
| `--model` | Model to use for all agents | llama3 |
| `--agent-dir` | Directory containing agent code | debate_day/agents |
| `--pro-name` / `--pro_name` | Name for the Pro agent | Alex |
| `--con-name` / `--con_name` | Name for the Con agent | Ben |
| `--mod-name` / `--mod_name` | Name for the Moderator agent | Mia |
| `--port` | Port for the MCP server | 8000 |
| `--host` | Host for the MCP server | localhost |
| `--wait` | Seconds to wait for MCP server to start | 5 |

### Examples

1. Run a debate with the default settings:
   ```bash
   python cli_tools/run_debate.py
   ```

2. Run a debate with a custom topic and 2 rounds:
   ```bash
   python cli_tools/run_debate.py --topic "Democracy is the best form of government" --rounds 2
   ```

3. Run a debate with custom agent names:
   ```bash
   python cli_tools/run_debate.py --pro-name Alice --con-name Bob --mod-name Charlie
   ```

4. Run a debate with a custom server port:
   ```bash
   python cli_tools/run_debate.py --port 8080
   ```

### What it Does

1. Starts the MCP server in a subprocess
2. Waits for the server to be ready
3. Creates a new debate via the MCP API
4. Sets up environment files for all agents
5. Launches all agent processes
6. Monitors output from all processes
7. Handles graceful shutdown when terminated

## view_debate.py

The `view_debate.py` script provides a real-time viewer for ongoing debates. It connects to the MCP server, polls for updates, and displays the debate progress in a human-readable format with color coding.

### Prerequisites

- MCP server running (see `debate_day/run_mcp_server.py`)
- An existing debate (created via `start_debate.py` or `run_debate.py`)
- Required Python packages:
  ```
  httpx
  ```

### Usage

```bash
python cli_tools/view_debate.py --debate-id YOUR_DEBATE_ID
```

### Command-line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--debate-id` / `--debate_id` | ID of the debate to view (required) | - |
| `--mcp-url` | URL of the MCP server | http://localhost:8000 |
| `--refresh` | Refresh interval in seconds | 2.0 |
| `--clear` | Clear the terminal between refreshes | False |

### Examples

1. View a debate with the default settings:
   ```bash
   python cli_tools/view_debate.py --debate-id test-debate-id-001
   ```

2. View a debate with faster refresh rate:
   ```bash
   python cli_tools/view_debate.py --debate-id test-debate-id-001 --refresh 1.0
   ```

3. View a debate with terminal clearing for cleaner display:
   ```bash
   python cli_tools/view_debate.py --debate-id test-debate-id-001 --clear
   ```

4. Connect to a custom MCP server:
   ```bash
   python cli_tools/view_debate.py --debate-id test-debate-id-001 --mcp-url http://192.168.1.100:8000
   ```

### What it Does

1. Connects to the MCP server and retrieves debate information
2. Displays debate status, current round, and next speaker
3. Shows all debate messages organized by round with color coding:
   - PRO messages in green
   - CON messages in red
   - MODERATOR messages in yellow
   - SYSTEM messages in cyan
4. Automatically refreshes the display when new messages appear
5. Shows the final verdict and winner when the debate concludes
6. Handles graceful termination on Ctrl+C

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

## launch_agents.py

The `launch_agents.py` script simplifies launching one or all debate agents for an existing debate. Use this when you need to launch agents separately or restart a specific agent.

### Usage

```bash
python cli_tools/launch_agents.py --debate-id test-debate-id-001
```

### Command-line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--debate-id` / `--debate_id` | ID of the existing debate (required) | - |
| `--role` | Agent role to launch (pro, con, mod, or all) | all |
| `--model` | Model to use for the agent(s) | llama3 |
| `--mcp-url` | URL of the MCP server | http://localhost:8000 |
| `--agent-dir` | Directory containing agent code | debate_day/agents |
| `--pro-name` / `--pro_name` | Name for the Pro agent | Alex |
| `--con-name` / `--con_name` | Name for the Con agent | Ben |
| `--mod-name` / `--mod_name` | Name for the Moderator agent | Mia |
| `--debug` | Enable debug mode with more verbose output | False |
| `--no-checks` | Skip pre-launch checks (MCP server and Ollama) | False |

### Examples

1. Launch all agents for an existing debate:
   ```bash
   python cli_tools/launch_agents.py --debate-id test-debate-id-001
   ```

2. Launch only the Pro agent:
   ```bash
   python cli_tools/launch_agents.py --debate-id test-debate-id-001 --role pro
   ```

3. Launch only the Moderator agent with a custom name:
   ```bash
   python cli_tools/launch_agents.py --debate-id test-debate-id-001 --role mod --mod-name Charlie
   ```

4. Launch with debug mode for troubleshooting:
   ```bash
   python cli_tools/launch_agents.py --debate-id test-debate-id-001 --debug
   ```

5. Skip connectivity checks and force launch:
   ```bash
   python cli_tools/launch_agents.py --debate-id test-debate-id-001 --no-checks
   ```

### What it Does

1. Performs pre-launch checks (unless `--no-checks` is specified):
   - Verifies the MCP server is running and accessible
   - Checks that Ollama is running
   - Validates that agent code exists and has required files
2. Creates/overwrites `.env` files in the selected agent directories
3. Launches the specified agent(s) as subprocesses
4. Monitors and displays agent output
5. Handles graceful termination on Ctrl+C

### Debugging Tips

If agents fail to start:
1. Run with the `--debug` flag to get more detailed output
2. Check that the MCP server is running at the specified URL
3. Verify that Ollama is running with the specified model
4. Ensure agent directories exist at the specified path
5. Check agent logs for specific errors
6. Try running with `--no-checks` to bypass connectivity tests 