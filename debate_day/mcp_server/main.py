"""
Main application for the Debate Day MCP server.

This module initializes the FastAPI application, registers routes,
and configures middleware and other application settings.
"""

import os
import logging
from typing import Dict, Any

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from debate_day.mcp_server.routes import get_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)
logger = logging.getLogger("mcp_server")

# Create FastAPI application
app = FastAPI(
    title="Debate Day 2.0 - MCP Server",
    description="Central communication hub for the Debate Day 2.0 system",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(get_router())

# Error handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """
    Handle validation errors in a cleaner way.
    
    Args:
        request: The request that caused the error
        exc: The validation error
        
    Returns:
        JSON response with error details
    """
    errors = exc.errors()
    error_messages = []
    
    for error in errors:
        field = ".".join(str(loc) for loc in error["loc"])
        message = error["msg"]
        error_messages.append(f"{field}: {message}")
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": "Validation error",
            "errors": error_messages
        }
    )

# Root endpoint
@app.get("/")
async def root() -> Dict[str, Any]:
    """
    Root endpoint with basic server information.
    
    Returns:
        Basic server information
    """
    return {
        "name": "Debate Day 2.0 - MCP Server",
        "version": "1.0.0",
        "status": "running",
        "endpoints": [
            {"path": "/api/start", "method": "POST", "description": "Start a new debate"},
            {"path": "/api/message/{debate_id}", "method": "POST", "description": "Add a message to a debate"},
            {"path": "/api/context/{debate_id}", "method": "GET", "description": "Get message history"},
            {"path": "/api/turn/{debate_id}", "method": "GET", "description": "Get turn information"},
            {"path": "/api/status/{debate_id}", "method": "GET", "description": "Get debate status"},
            {"path": "/api/debates", "method": "GET", "description": "List all debates"},
            {"path": "/api/debate/{debate_id}", "method": "GET", "description": "Get detailed debate information"}
        ],
        "docs_url": "/docs"
    }

# Health check endpoint
@app.get("/health")
async def health_check() -> Dict[str, str]:
    """
    Health check endpoint.
    
    Returns:
        Health status information
    """
    return {"status": "healthy"}

# Default port
DEFAULT_PORT = 8000

if __name__ == "__main__":
    """Run the application directly."""
    import uvicorn
    
    # Get port from environment or use default
    port = int(os.environ.get("PORT", DEFAULT_PORT))
    
    # Run the application
    logger.info(f"Starting MCP server on port {port}")
    uvicorn.run(
        "debate_day.mcp_server.main:app",
        host="0.0.0.0",
        port=port,
        reload=True  # Enable auto-reload for development
    ) 