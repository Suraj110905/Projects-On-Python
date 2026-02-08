# 🚀 Quick Start Guide

Get up and running with WhatsApp Chat Analyzer in 3 simple steps!

## Step 1: Install Dependencies

Open your terminal in the project directory and run:

```bash
pip install -r requirements.txt
```

This will install all required packages including:
- pandas, numpy (data processing)
- matplotlib, seaborn, plotly (visualizations)
- streamlit (web dashboard)
- emoji, vaderSentiment, textblob (NLP)
- wordcloud (word clouds)

## Step 2: Export Your WhatsApp Chat

### On Android:
1. Open WhatsApp and the chat you want to analyze
2. Tap the three dots (⋮) → More → Export chat
3. Choose "Without media"
4. Save the `.txt` file

### On iOS:
1. Open WhatsApp and the chat you want to analyze
2. Tap the contact/group name at the top
3. Scroll down and tap "Export Chat"
4. Choose "Without Media"
5. Save the `.txt` file

## Step 3: Run the Dashboard

### Option A: Using the batch file (Windows)
Double-click `run_dashboard.bat`

### Option B: Using command line
```bash
streamlit run src/whatsapp_analyzer/app.py
```

### Option C: Using Python directly
```bash
python -m streamlit run src/whatsapp_analyzer/app.py
```

The dashboard will open in your web browser automatically!

## 📊 Using the Dashboard

1. **Upload your chat file** using the sidebar file uploader
2. **Explore the tabs**:
   - 👥 User Stats - Message counts and distributions
   - 📈 Activity - Timeline and time-based patterns
   - 😀 Emojis - Emoji usage analysis
   - 💬 Words - Word frequency and word clouds
   - 🎭 Sentiment - Sentiment analysis results
   - ⚡ Response Times - Response time calculations

## 🐍 Using the Python API

If you prefer programmatic access:

```python
from whatsapp_analyzer import ChatParser, ChatAnalyzer, ChatVisualizer

# Load and parse chat
parser = ChatParser('path/to/your/chat.txt')
df = parser.load_chat()

# Analyze
analyzer = ChatAnalyzer(df)
stats = analyzer.get_user_stats()
emojis = analyzer.analyze_emojis()

# Visualize
visualizer = ChatVisualizer()
fig = visualizer.plot_user_message_distribution(stats)
```

## 🧪 Run Tests

To verify everything is working:

```bash
pytest tests/ -v
```

## 💡 Tips

- **Large chats**: The app works best with chats containing 100-10,000 messages
- **Privacy**: All analysis is done locally on your machine
- **Multiple chats**: You can analyze different chats by uploading new files
- **Sample data**: Try the included sample chat in `data/sample/sample_chat.txt`

## 🆘 Troubleshooting

**Dashboard won't start?**
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Check you're in the correct directory
- Try: `python -m streamlit run src/whatsapp_analyzer/app.py`

**Chat won't parse?**
- Ensure the file is a .txt WhatsApp export
- Check the file is not empty
- Verify the format matches WhatsApp's export format

**Missing dependencies?**
- Run: `pip install --upgrade -r requirements.txt`

## 📚 Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check out the example analyses in the notebooks folder (coming soon)
- Explore the source code in `src/whatsapp_analyzer/`

---

**Need help?** Open an issue on GitHub or check the documentation!

**Enjoy analyzing your chats! 💬📊**
