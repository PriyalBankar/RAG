#!/usr/bin/env python3
"""
Simple script to run the FastAPI backend server
"""
import uvicorn
import sys
import os
from utilities.constants import API_HOST, API_PORT

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    uvicorn.run("api.main:app", host=API_HOST, port=API_PORT, reload=True)
