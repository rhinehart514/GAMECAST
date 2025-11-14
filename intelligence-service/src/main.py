"""
Intelligence Service - Main Entry Point

Run this to start the intelligence API service.
"""

import uvicorn
from api.endpoints import app


if __name__ == "__main__":
    print("=" * 70)
    print("NHL Intelligence Service")
    print("=" * 70)
    print("\nStarting server...")
    print("API docs will be available at: http://localhost:5001/docs")
    print("Health check: http://localhost:5001/health")
    print("\nPress Ctrl+C to stop\n")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=5001,
        log_level="info"
    )

