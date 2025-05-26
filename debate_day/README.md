# Debate Day

A lightweight multi-agent system where two AI agents debate a topic from opposing viewpoints.

---

## Features

- **User-defined Topics** – Input any topic for the AI agents to debate.
- **Pro and Con Agents** – Ava (Pro) argues in support of the topic, while Ben (Con) argues against it.
- **Turn-based Debate** – Arguments are generated sequentially by each agent.
- **Local LLM Support** – Uses Ollama for local LLM integration, supporting models like TinyLlama and Llama3.

---

## Tech stack

- Python
- [CrewAI](https://docs.crewai.com)
- [Ollama](https://ollama.ai) for local LLM integration
- LangChain for LLM interaction

---

## Architecture

The project follows a modular structure:

```
debate_day/
├── agents/
│   ├── pro_agent.py  # Defines the Pro agent (Ava)
│   ├── con_agent.py  # Defines the Con agent (Ben)
│   └── mod_agent.py  # Defines the Moderator agent (Mia)
├── crew/
│   └── debate_crew.py # Defines the CrewAI setup and how agents collaborate
├── tasks/
│   ├── pro_task.py   # Defines the task for the Pro agent
│   ├── con_task.py   # Defines the task for the Con agent
│   └── mod_task.py   # Defines the task for the Moderator
├── main.py             # Orchestrates the debate, handles user input and initiates the crew
├── requirements.txt    # Lists project dependencies
└── README.md          # This file
```

---

## Setup the application
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Install and start Ollama:
   - Visit [Ollama's website](https://ollama.ai) for installation instructions
   - Start the Ollama server (it should run on http://localhost:11434)
   - Pull the required model: `ollama pull tinyllama` (or `ollama pull llama3` for better quality)

---

## Run the application
1. Make sure Ollama is running and the model is downloaded
2. Execute the main script: `python main.py`
3. The script will first run a minimal test to verify the setup
4. You will then be prompted to enter a debate topic

---

## Configuration
The application uses the following default settings (configurable in main.py):
- Default model: TinyLlama (faster but lower quality)
- Alternative model: Llama3 (higher quality but slower)
- Ollama server URL: http://localhost:11434
- Temperature: 0.7 (controls creativity vs consistency)

---

## Troubleshooting
If you encounter issues:
1. Ensure Ollama is running (`ollama serve`)
2. Verify the model is downloaded (`ollama list`)
3. Check the logs for detailed error messages
4. Make sure all dependencies are installed correctly

---

## License
MIT
