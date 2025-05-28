#!/usr/bin/env python3
"""
Run script for the MCP server.

This script provides a convenient way to start the MCP server
with command-line options.
"""

import os
import argparse
import uvicorn
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)
logger = logging.getLogger("run_mcp_server")

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Start the Debate Day MCP server"
    )
    
    parser.add_argument(
        "--host", 
        type=str,
        default="0.0.0.0",
        help="Host to bind the server to (default: 0.0.0.0)"
    )
    
    parser.add_argument(
        "--port", 
        type=int,
        default=8000,
        help="Port to bind the server to (default: 8000)"
    )
    
    parser.add_argument(
        "--reload",
        action="store_true",
        help="Enable auto-reload for development"
    )
    
    parser.add_argument(
        "--log-level",
        type=str,
        default="info",
        choices=["debug", "info", "warning", "error", "critical"],
        help="Logging level (default: info)"
    )
    
    return parser.parse_args()

def main():
    """Run the MCP server."""
    args = parse_args()
    
    # Set log level
    log_level = getattr(logging, args.log_level.upper())
    logging.getLogger().setLevel(log_level)
    
    # Print startup message
    logger.info(f"Starting MCP server on {args.host}:{args.port}")
    logger.info(f"Log level: {args.log_level.upper()}")
    logger.info(f"Auto-reload: {'enabled' if args.reload else 'disabled'}")
    
    # Run the server
    uvicorn.run(
        "debate_day.mcp_server.main:app",
        host=args.host,
        port=args.port,
        reload=args.reload,
        log_level=args.log_level.lower()
    )

if __name__ == "__main__":
    main() 