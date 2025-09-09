#!/usr/bin/env python3
"""
WSGI entry point for UzIPTV application
"""

import os
import sys

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from main import app

if __name__ == "__main__":
    app.run()
