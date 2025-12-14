"""
Simple startup script for the Python HTTP server
Run this on Hostinger: python start.py
"""
from server import run_server
import os

# Get port from environment or use default
port = int(os.getenv('PORT', 8000))
run_server(port)

