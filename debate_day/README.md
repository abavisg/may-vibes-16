# Debate Day

A lightweight multi-agent system where two AI agents debate a topic from opposing viewpoints.

---

## Features

- **User-defined Topics** – Input any topic for the AI agents to debate.
- **Pro and Con Agents** – Ava (Pro) argues in support of the topic, while Ben (Con) argues against it.
- **Turn-based Debate** – Arguments are generated sequentially by each agent.

---

## Tech stack

- Python
- [CrewAI](https://docs.crewai.com)
- Optional: LM Studio or Ollama for local LLM integration

---

## Architecture

The project follows a modular structure:

```
debate_day/
├── agents/
│   ├── pro_agent.py  # Defines the Pro agent (Ava)
│   └── con_agent.py  # Defines the Con agent (Ben)
├── crew/
│   └── debate_crew.py # Defines the CrewAI setup and how agents collaborate
├── tasks/
│   ├── pro_task.py   # Defines the task for the Pro agent
│   └── con_task.py   # Defines the task for the Con agent
├── main.py             # Orchestrates the debate, handles user input and initiates the crew
├── requirements.txt    # Lists project dependencies
└── README.md           # This file
```

---

## API Endpoints
Currently, there are no API endpoints as this is a CLI-based application.

---

## Setup the application
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Configure your LLM provider (e.g., OpenAI API key, or local Ollama/LM Studio setup).

---

## Run the application
Execute the main script: `python main.py`
You will be prompted to enter a debate topic.

---

## License
MIT
