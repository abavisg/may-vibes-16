# Debate Day

A command-line application that simulates a debate between AI agents using local LLM models, with a modern Flutter web UI for real-time debate visualization.

## Features

- **Real-time debate visualization**: Watch AI agents debate in a modern web interface
- **Automatic agent management**: Agents are automatically launched when debates are created
- **Debate between Pro and Con AI agents** on any topic with configurable rounds (1-10)
- **Impartial moderator evaluation** with declared winner
- **Local LLM integration** using Ollama models for dynamic AI-driven content
- **Fallback responses** if LLM is unavailable
- **Comprehensive logging** saved to `logs/` directory
- **MCP server** for centralized debate management
- **Autonomous agent architecture** with modular design
- **CLI tools** for orchestrating debates
- **Modern Flutter UI** with responsive design and real-time updates
- **Personalized AI agents**: Meet Ava (Pro), Ben (Con), and Mia (Moderator) with custom avatars

## Meet the Debate Team

🎭 **Ava** - Pro Agent (Female)
- Argues in favor of the debate topic
- Expert at presenting compelling evidence and logical arguments
- Shown on the left side of the debate interface in blue

👨‍💼 **Ben** - Con Agent (Male)  
- Argues against the debate topic
- Skilled at finding counterpoints and challenging assumptions
- Shown on the right side of the debate interface in red

👩‍⚖️ **Mia** - Moderator (Female)
- Impartial judge who evaluates both sides
- Provides thoughtful analysis and declares the winner
- Shown at the bottom of the interface in amber/yellow

## Recent Updates (v2.2)

- ✅ **Fixed rounds bug**: Debates now properly run for the requested number of rounds (1-10)
- ✅ **Improved UI layout**: More compact design with better space utilization
- ✅ **Enhanced moderator panel**: Left-aligned, compact layout with clear status indicators
- ✅ **Automatic agent launching**: No more manual agent management required
- ✅ **Real-time updates**: Live debate progress in the Flutter UI
- ✅ **Personalized agents**: Custom names and professional avatar images
- ✅ **Compact fonts**: Smaller, more readable text throughout the interface
- ✅ **Fixed rounds logic**: Corrected issue where selecting 5 rounds only resulted in 2-3 actual rounds
- ✅ **Codebase cleanup**: Removed legacy CrewAI components and unnecessary files
- ✅ **Consolidated documentation**: Single comprehensive README
- ✅ **Code quality improvements**: Fixed all Flutter/Dart linting issues for cleaner, more maintainable code
  - Resolved cascade invocations optimization in API service
  - Converted block function bodies to expression bodies where appropriate
  - Added proper type annotations for better type safety
  - Improved code formatting and line length compliance

## Architecture

The system uses an **Autonomous Agent Architecture** with standalone agents that communicate via the MCP server:

- **MCP Server**: FastAPI-based central server for debate management
- **Protocol**: Defines message formats and standardizes communication
- **Agent Modules**: Self-contained agent implementations in dedicated directories
- **CLI Tools**: Utilities for starting debates and managing agents
- **Flutter Web UI**: Modern web interface for real-time debate visualization

## Requirements

- Python 3.9+
- Ollama (running locally with llama3 model)
- FastAPI and uvicorn (for MCP server)
- httpx for HTTP requests
- loguru for logging
- Flutter/Dart SDK (for the web UI)

## Getting Started

### Prerequisites

- Python 3.9+
- Flutter/Dart SDK (for the Flutter UI)
- Ollama with llama3 model installed

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd debate-day-2.0
```

2. Install the package:
```bash
pip install -e .
```

3. Start Ollama with the required model:
```bash
ollama run llama3
```

4. Start the MCP server:
```bash
python debate_day/run_mcp_server.py --reload
```

The MCP server will now **automatically launch agents** whenever a new debate is created from the Flutter UI!

### Running the Flutter UI

1. Navigate to the Flutter app:
```bash
cd debate_day/flutter_ui/debate_day_web
```

2. Install dependencies:
```bash
flutter pub get
```

3. Run the app:
```bash
flutter run -d chrome
```

### How It Works

1. **Start a Debate**: Use the Flutter UI to enter a topic and number of rounds
2. **Automatic Agent Launch**: The MCP server automatically:
   - Creates the debate with a unique ID
   - Configures each agent with the debate ID
   - Launches the pro, con, and moderator agents
3. **Watch the Debate**: The agents will automatically participate in the debate, which you can watch in real-time in the Flutter UI

## CLI Tools

The `cli_tools/` directory contains command-line utilities for managing debates:

### run_debate.py

All-in-one solution that handles the entire debate workflow:

```bash
python cli_tools/run_debate.py --topic "AI will benefit humanity" --rounds 3
```

**Options:**
- `--topic`: The debate topic/resolution
- `--rounds`: Number of debate rounds (1-10)
- `--model`: Model to use for all agents (default: llama3)
- `--pro-name`: Name for the Pro agent (default: Ava)
- `--con-name`: Name for the Con agent (default: Ben)
- `--mod-name`: Name for the Moderator agent (default: Mia)
- `--port`: Port for the MCP server (default: 8000)

### start_debate.py

Initialize a new debate via the MCP server:

```bash
python cli_tools/start_debate.py --topic "Democracy is the best form of government" --rounds 2 --launch-agents
```

### view_debate.py

Real-time viewer for ongoing debates:

```bash
python cli_tools/view_debate.py --debate-id YOUR_DEBATE_ID
```

### launch_agents.py

Launch agents for an existing debate:

```bash
python cli_tools/launch_agents.py --debate-id YOUR_DEBATE_ID --role all
```

## Flutter Web UI

### Features

- Create debates on any topic with 1-10 rounds
- Watch AI agents debate in real-time
- Pro and Con positions presented visually
- Moderated debate format with winner declaration
- Responsive design with modern UI
- Real-time polling for updates
- Comprehensive error handling

### Architecture

- **Flutter for Web**: Cross-platform UI framework
- **Provider**: Simple state management
- **HTTP**: REST API communication with the Python backend
- **Extensive Error Handling**: Robust error catching and logging

### Project Structure

```
lib/
├── main.dart                // App entry point and theming
├── pages/
│   └── debate_page.dart     // Main vertical split UI
├── widgets/
│   ├── avatar_widget.dart   // Agent avatar display
│   ├── message_bubble.dart  // Message display widget
│   └── toolbar.dart         // Top toolbar with debate controls
├── models/
│   └── debate_models.dart   // Data models for debate entities
└── services/
    └── api_service.dart     // REST API client for backend
```

### API Integration

The Flutter app communicates with the backend API:

- `POST /api/start` - Start a new debate
- `GET /api/context/{debate_id}` - Get message history
- `GET /api/turn/{debate_id}` - Check whose turn it is
- `GET /api/status/{debate_id}` - Check debate status
- `GET /api/debate/{debate_id}` - Get detailed debate info

## Agent System

### Agent Configuration

Each agent is configured via `.env` files:

```
ROLE=pro                            # Agent role (pro/con/mod)
MODEL=llama3                        # Ollama model to use
MCP_SERVER_URL=http://localhost:8000 # MCP server URL
AGENT_NAME=Ava                      # Agent's display name
DEBATE_ID=debate-id-here            # Debate to participate in
```

### Agent Features

- **Automatic polling** of MCP server to determine turns
- **Context-aware prompts** based on debate history
- **Round-specific strategies** for initial arguments vs rebuttals
- **Ollama integration** for LLM-powered responses
- **Comprehensive logging** for debugging
- **Graceful error handling** with fallback responses

### Agent Strategies

**Pro Agent (Ava):**
- Round 0: Strong initial arguments in favor
- Later rounds: Rebuttals addressing Con's points while reinforcing Pro position

**Con Agent (Ben):**
- Round 0: Critical counter-arguments against the topic
- Later rounds: Targeted rebuttals pointing out flaws in Pro's reasoning

**Moderator (Mia):**
- Evaluates all arguments from both sides
- Considers strength, coherence, evidence quality, and persuasiveness
- Declares winner with justification

## Sample Topics

- Did we ever go to the moon?
- Should artificial intelligence be regulated by governments?
- Is remote work better than office work?
- Democracy is the best form of government
- Climate change requires immediate action

## Troubleshooting

### Issue: Agents not participating in debates

**Problem**: Agents aren't responding after creating a debate in the Flutter UI.

**Solutions**:

1. **Check MCP Server**: Ensure the MCP server is running with the latest code:
   ```bash
   python debate_day/run_mcp_server.py --reload
   ```

2. **Check Ollama**: Make sure Ollama is running with the llama3 model:
   ```bash
   ollama list  # Should show llama3
   ollama run llama3  # If not running
   ```

3. **Check Agent Logs**: Look in the `logs/` directory for agent-specific error messages

4. **Manual Agent Launch** (if automatic launch fails):
   Find the debate ID from the Flutter UI and run:
   ```bash
   python3 cli_tools/launch_agents.py \
       --debate-id "YOUR_DEBATE_ID" \
       --role all
   ```

### Issue: MCP Server Connection Errors

**Problem**: Flutter UI shows "API server appears to be offline"

**Solution**: 
- Ensure the MCP server is running on `http://localhost:8000`
- Check that no firewall is blocking port 8000
- Try accessing `http://localhost:8000/docs` in your browser

### Issue: Wrong number of rounds

**Problem**: Selecting 5 rounds but only getting 1-2 rounds

**Solution**: This has been fixed in v2.2. Make sure you're using the latest code and restart the MCP server.

## Development

### Project Structure

```
debate_day/
├── mcp_server/          # FastAPI server and database
├── protocol/            # Message formats and communication protocol
├── agents/              # Autonomous agent implementations
│   ├── pro/            # Pro agent (Ava)
│   ├── con/            # Con agent (Ben)
│   └── mod/            # Moderator agent (Mia)
├── flutter_ui/         # Flutter web application
│   └── debate_day_web/ # Main Flutter app
└── run_mcp_server.py   # MCP server launcher

cli_tools/
├── run_debate.py       # All-in-one debate runner
├── start_debate.py     # Debate initializer
├── view_debate.py      # Real-time debate viewer
└── launch_agents.py    # Agent launcher
```

### Adding New Features

1. **New Agent Types**: Add new directories under `debate_day/agents/`
2. **UI Enhancements**: Modify Flutter components in `debate_day/flutter_ui/debate_day_web/lib/`
3. **API Extensions**: Add new endpoints in `debate_day/mcp_server/routes.py`
4. **Protocol Changes**: Update message formats in `debate_day/protocol/`

## License

MIT License - see LICENSE file for details. 