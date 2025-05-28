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
    echo "  --legacy     Run the legacy CrewAI-based application"
    echo "  --mcp        Run the MCP server"
    echo "  --debate     Run a new debate with the CLI tool"
    echo "  --help       Display this help message"
    echo ""
    echo "Examples:"
    echo "  ./run_debug.sh --legacy        # Run the legacy application"
    echo "  ./run_debug.sh --mcp           # Run the MCP server"
    echo "  ./run_debug.sh --debate        # Run a new debate with default settings"
    echo ""
}

# Parse command-line arguments
if [ $# -eq 0 ]; then
    echo "No options specified. Use --help for usage information."
    exit 1
fi

for arg in "$@"; do
    case $arg in
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
        --help)
            print_usage
            exit 0
            ;;
        *)
            echo "Unknown option: $arg"
            print_usage
            exit 1
            ;;
    esac
done

echo "-----------------------------------------------------------------"
echo "Debate Day app finished." 