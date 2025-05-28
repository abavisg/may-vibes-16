#!/bin/bash
# Script to run the Debate Day app in debug/development mode.
# This uses the LLM settings (e.g., tinyllama by default) and verbosity configured in the Python scripts.

# Get the directory where the script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"

APP_DIR="$SCRIPT_DIR/debate_day"
CLI_DIR="$SCRIPT_DIR/cli_tools"

# Function to print usage information
function print_usage() {
    echo "Usage: ./run_debug.sh [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  --all-in-one  Run the all-in-one debate system (recommended)"
    echo "  --legacy      Run the legacy CrewAI-based application"
    echo "  --mcp         Run the MCP server"
    echo "  --debate      Run a new debate with the CLI tool"
    echo "  --launch      Launch agents for an existing debate"
    echo "  --help        Display this help message"
    echo ""
    echo "Examples:"
    echo "  ./run_debug.sh --all-in-one                   # Run the complete system in one step"
    echo "  ./run_debug.sh --legacy                       # Run the legacy application"
    echo "  ./run_debug.sh --mcp                          # Run the MCP server"
    echo "  ./run_debug.sh --debate                       # Run a new debate with default settings"
    echo "  ./run_debug.sh --launch --debate-id=my-debate # Launch agents for an existing debate"
    echo ""
}

# Parse command-line arguments
if [ $# -eq 0 ]; then
    echo "No options specified. Running all-in-one debate system (recommended)."
    cd "$SCRIPT_DIR" || {
        echo "Error: Could not navigate to $SCRIPT_DIR."
        exit 1
    }
    python3 cli_tools/run_debate.py
    exit 0
fi

DEBATE_ID=""

for arg in "$@"; do
    # Check for --debate-id parameter
    if [[ $arg == --debate-id=* ]]; then
        DEBATE_ID="${arg#*=}"
        continue
    fi
    
    case $arg in
        --all-in-one)
            echo "Running all-in-one debate system..."
            cd "$SCRIPT_DIR" || {
                echo "Error: Could not navigate to $SCRIPT_DIR."
                exit 1
            }
            python3 cli_tools/run_debate.py
            ;;
        --legacy)
            echo "Running legacy CrewAI-based application..."
            cd "$APP_DIR" || {
                echo "Error: Could not navigate to $APP_DIR."
                exit 1
            }
            python3 main.py
            ;;
        --mcp)
            echo "Running MCP server..."
            cd "$APP_DIR" || {
                echo "Error: Could not navigate to $APP_DIR."
                exit 1
            }
            python3 run_mcp_server.py
            ;;
        --debate)
            echo "Starting a new debate..."
            cd "$SCRIPT_DIR" || {
                echo "Error: Could not navigate to $SCRIPT_DIR."
                exit 1
            }
            python3 cli_tools/start_debate.py --topic "Is artificial intelligence beneficial for humanity?" --rounds 1 --launch-agents
            ;;
        --launch)
            echo "Launching agents for existing debate..."
            if [ -z "$DEBATE_ID" ]; then
                echo "Error: --debate-id parameter is required for --launch option."
                echo "Example: ./run_debug.sh --launch --debate-id=my-debate-id"
                exit 1
            fi
            cd "$SCRIPT_DIR" || {
                echo "Error: Could not navigate to $SCRIPT_DIR."
                exit 1
            }
            python3 cli_tools/launch_agents.py --debate-id "$DEBATE_ID"
            ;;
        --help)
            print_usage
            exit 0
            ;;
        *)
            # Skip arguments that start with --debate-id as they're handled above
            if [[ $arg != --debate-id=* ]]; then
                echo "Unknown option: $arg"
                print_usage
                exit 1
            fi
            ;;
    esac
done

echo "-----------------------------------------------------------------"
echo "Debate Day app finished." 