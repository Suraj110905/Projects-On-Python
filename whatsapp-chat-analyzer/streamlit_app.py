"""Streamlit Cloud Entry Point for WhatsApp Chat Analyzer."""

import sys
from pathlib import Path

# Add src directory to Python path for imports
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

# Now import the main app module content
import streamlit as st
import pandas as pd

from whatsapp_analyzer.parser import ChatParser
from whatsapp_analyzer.analyzer import ChatAnalyzer
from whatsapp_analyzer.visualizer import ChatVisualizer
from whatsapp_analyzer.group_analyzer import GroupChatAnalyzer

# Import the main function from app and execute it
from whatsapp_analyzer import app

# Run the app
app.main()
