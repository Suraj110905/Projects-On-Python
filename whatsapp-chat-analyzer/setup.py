"""Setup script for WhatsApp Chat Analyzer."""

from setuptools import setup, find_packages

setup(
    name="whatsapp-chat-analyzer",
    version="0.1.0",
    description="Comprehensive WhatsApp chat analysis tool with visualization and insights",
    author="Suraj Kumar",
    author_email="suraj110905@gmail.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.9",
    install_requires=[
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "emoji>=2.10.0",
        "textblob>=0.17.0",
        "vaderSentiment>=3.3.2",
        "matplotlib>=3.7.0",
        "seaborn>=0.13.0",
        "plotly>=5.18.0",
        "wordcloud>=1.9.0",
        "streamlit>=1.29.0",
        "python-dateutil>=2.8.2",
        "pytz>=2023.3",
    ],
)
