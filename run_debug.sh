#!/bin/bash
# Script to run the Debate Day app in debug/development mode.
# This uses the LLM settings (e.g., tinyllama by default) and verbosity configured in the Python scripts.

# Get the directory where the script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"

APP_DIR="$SCRIPT_DIR/debate_day"

# export LITELLM_LOG="DEBUG" # No longer needed, LangChain debug is set in main.py
# echo "LITELLM_LOG set to DEBUG by run_debug.sh" # No longer needed

echo "Navigating to application directory: $APP_DIR"
cd "$APP_DIR" || {
    echo "Error: Could not navigate to $APP_DIR. Make sure the debate_day directory exists relative to this script."
    exit 1
}

echo ""
# export LANGCHAIN_DEBUG=true # No longer explicitly using LangChain direct debug for this setup

echo "Running Debate Day app (main.py)..."
echo "(Using Ollama model: tinyllama by default. Edit debate_day/main.py to change.)"
echo "(LLM configured via environment variables set in main.py)"
echo "-----------------------------------------------------------------"
python3 main.py

echo "-----------------------------------------------------------------"
echo "Debate Day app finished." 