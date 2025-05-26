# Debate Day

A lightweight multi-agent system where two AI agents debate a topic from opposing viewpoints.

---

## Features

- **User-defined Topics** – Enter any debate topic for the AI agents to discuss
- **Configurable Debate Depth** – Choose from 0-3 rebuttals per side to control debate complexity
- **Agent-Based Debate** – A Pro agent argues in support of the topic, while a Con agent argues against it, and a Moderator evaluates both arguments
- **Local LLM Support** – Uses Ollama for local LLM integration, supporting llama3 models for private, cost-effective AI
- **Sequential Process Flow** – Pro → Con → [Multiple rounds of rebuttals] → Moderator for a structured debate format

---

## Tech Stack

- Python
- [CrewAI](https://docs.crewai.com) for multi-agent orchestration
- [Ollama](https://ollama.ai) for local LLM integration with llama3

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
├── main.py           # Orchestrates the debate
├── requirements.txt  # Lists project dependencies
└── README.md         # This file
```

---

## Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Install and start Ollama:
   - Visit [Ollama's website](https://ollama.ai) for installation instructions
   - Start the Ollama server: `ollama serve`
   - Pull the llama3 model: `ollama pull llama3`

---

## Usage

1. Make sure Ollama is running with the llama3 model available
2. Run the application:
   ```
   python main.py
   ```
3. When prompted, enter a debate topic (or press Enter to use the default topic)
4. Choose the number of rebuttals each side should have:
   - **0 rebuttals**: Basic debate with one argument from each side
   - **1 rebuttal**: Standard debate with initial arguments and one rebuttal each
   - **2 rebuttals**: Extended debate with initial arguments and two rebuttals each
   - **3 rebuttals**: Full debate with initial arguments and three rebuttals each
5. The system will execute a debate on your chosen topic:
   - The Pro agent (Ava) will argue in favor of the topic
   - The Con agent (Ben) will present counterarguments
   - If using rebuttals, Ava and Ben will take turns responding to each other's points
   - The Moderator (Mia) will evaluate all points and declare a winner

---

## Example Topics

Here are some example debate topics you can try:
- "Should artificial intelligence be regulated by governments?"
- "Is remote work better than working in an office?"
- "Should universities prioritize online courses over traditional in-person classes?"
- "Is universal basic income a viable economic policy?"
- "Should social media platforms be held liable for user content?"

---

## Customization

To modify the application's behavior:
- Edit the system prompts in the agent files (pro_agent.py, con_agent.py, mod_agent.py)
- Update the task descriptions in the task files (pro_task.py, con_task.py, mod_task.py)
- Change the LLM model in main.py (e.g., from llama3 to another Ollama-supported model)
- Adjust the maximum number of rebuttals in main.py (currently capped at 3)

---

## License

This project is open-source. Feel free to use, modify, and distribute according to the terms of your chosen license.
