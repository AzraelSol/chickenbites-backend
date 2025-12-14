#!/usr/bin/env python3
"""
Simple entry point for Hostinger
This file can be executed directly by Hostinger's web server
"""
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

# Import and run server
from server import run_server

# Run on port 8000 (or get from environment)
port = int(os.getenv('PORT', 8000))
run_server(port)

