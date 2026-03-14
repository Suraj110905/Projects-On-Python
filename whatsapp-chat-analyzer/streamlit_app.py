"""Streamlit Cloud Entry Point for WhatsApp Chat Analyzer."""
import sys
import os
from pathlib import Path

# 1. Add the 'src' directory to Python path so 'import whatsapp_analyzer' works
current_dir = Path(__file__).parent
src_path = current_dir / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

import streamlit as st
import emoji  # Verifying the library is loaded from site-packages

# 2. Import the main function from your internal app logic
# This matches the folder structure: src/whatsapp_analyzer/app.py
from whatsapp_analyzer.app import main

if __name__ == "__main__":
    main()