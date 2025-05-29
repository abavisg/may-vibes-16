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

## Recent Updates (v2.1)

- ✅ **Fixed rounds bug**: Debates now properly run for the requested number of rounds (1-10)
- ✅ **Improved UI layout**: More compact design with better space utilization
- ✅ **Enhanced moderator panel**: Left-aligned, compact layout with clear status indicators
- ✅ **Automatic agent launching**: No more manual agent management required
- ✅ **Real-time updates**: Live debate progress in the Flutter UI
- ✅ **Personalized agents**: Custom names and professional avatar images
- ✅ **Compact fonts**: Smaller, more readable text throughout the interface
- ✅ **Fixed rounds logic**: Corrected issue where selecting 5 rounds only resulted in 2-3 actual rounds

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
*Note: This legacy version saved debate transcripts to an `outputs/` directory, which is now gitignored.*

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

## Architecture

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
*Note: This legacy version saved debate transcripts to an `outputs/` directory, which is now gitignored.*

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

## Development Process

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

## License

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