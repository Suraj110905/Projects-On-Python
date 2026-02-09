# 💬 WhatsApp Chat Analyzer

##  Project Overview

WhatsApp Chat Analyzer is a comprehensive Python-based data analysis tool designed to extract meaningful insights from WhatsApp chat exports. The project combines natural language processing, data visualization, and interactive web technologies to transform raw chat data into actionable analytics.

###  What Does This Project Do?

This tool takes a WhatsApp chat export file (the `.txt` file you get when exporting a conversation) and performs deep analysis to reveal:

- **Communication Patterns**: Who talks more? When are people most active? What days see the most conversation?
- **Emotional Tone**: Is the conversation generally positive, negative, or neutral?
- **Expression Analysis**: What emojis are used most? What words dominate the conversation?
- **Engagement Metrics**: How quickly do people respond to each other?
- **Visual Insights**: Beautiful charts, graphs, and word clouds that make data easy to understand

###  Why This Project?

WhatsApp is one of the world's most popular messaging platforms, with billions of conversations happening daily. However, WhatsApp itself provides limited analytical capabilities. This project fills that gap by:

1. **Preserving Privacy**: All analysis happens locally on your machine - no data is sent to external servers
2. **Providing Insights**: Understand relationship dynamics, communication habits, and conversation trends
3. **Being User-Friendly**: Both technical users (via Python API) and non-technical users (via web dashboard) can benefit
4. **Offering Flexibility**: Multiple analysis types and visualization options cater to different needs

###  Project Architecture

The project is built on a modular architecture with four main components:

#### 1. **Parser Module** (`parser.py`)
The foundation of the project - responsible for reading and interpreting WhatsApp chat files.

**Key Capabilities:**
- Recognizes multiple export formats (Android, iOS, 24-hour time, 12-hour time)
- Handles multiline messages that span multiple rows
- Identifies special message types (media, system notifications)
- Extracts metadata (timestamps, authors, message content)
- Converts raw text into structured pandas DataFrames

**How It Works:**
```
Raw Chat File → Regex Pattern Matching → Message Parsing → DataFrame Creation
```

#### 2. **Analyzer Module** (`analyzer.py`)
The brain of the project - performs all statistical and linguistic analysis.

**Analysis Categories:**

**a) User Statistics**
- Total messages per person
- Average message length and word count
- Media sharing frequency
- URL sharing patterns
- Activity percentages

**b) Temporal Analysis**
- Activity timeline (daily, weekly, monthly aggregations)
- Hourly activity patterns (when are users most active?)
- Day-of-week patterns (weekday vs weekend behavior)
- Most active days ranking

**c) Content Analysis**
- Emoji extraction and frequency counting
- Word frequency analysis with stop-word filtering
- Per-user content breakdowns

**d) Sentiment Analysis**
- Uses VADER (Valence Aware Dictionary and sEntiment Reasoner)
- Classifies messages as positive, neutral, or negative
- Provides compound sentiment scores (-1 to +1 scale)
- Per-user sentiment profiles

**e) Engagement Metrics**
- Response time calculations between users
- Mean, median, and standard deviation of response times
- Identifies fast vs slow responders

#### 3. **Visualizer Module** (`visualizer.py`)
The artistic component - transforms data into visual stories.

**Visualization Types:**

**Static Visualizations (Matplotlib/Seaborn):**
- Bar charts for message distributions
- Pie charts for proportional representation
- Heatmaps for hourly/daily activity patterns
- Horizontal bar charts for rankings
- Word clouds for text visualization

**Interactive Visualizations (Plotly):**
- Time series line charts with hover tooltips
- Multi-series comparisons
- Zoom and pan capabilities
- Export to PNG functionality
- Responsive layouts

**Dashboard Visualizations:**
- Tabbed interface for organized presentation
- Real-time rendering
- Customizable parameters (frequency, top N, etc.)

#### 4. **Dashboard Application** (`app.py`)
The user interface - makes the tool accessible to everyone.

**Features:**
- **File Upload**: Drag-and-drop or browse for chat files
- **Real-time Processing**: Instant analysis as files are uploaded
- **Organized Tabs**: Six specialized views for different analysis types
- **Interactive Controls**: Sliders, dropdowns for customization
- **Responsive Design**: Works on different screen sizes
- **Error Handling**: Graceful handling of invalid files or parsing issues

###  Technical Deep Dive

#### Data Processing Pipeline

```
1. File Upload
   ↓
2. Text Parsing (regex-based pattern matching)
   ↓
3. Data Structuring (pandas DataFrame)
   ↓
4. Feature Engineering (time features, emoji extraction, etc.)
   ↓
5. Analysis Execution (statistical computations)
   ↓
6. Visualization Generation
   ↓
7. Dashboard Display
```

#### Key Technologies Explained

**pandas**: Provides the DataFrame structure for efficient data manipulation. Enables powerful grouping, aggregation, and time-series operations.

**VADER Sentiment Analysis**: A lexicon and rule-based sentiment analyzer specifically tuned for social media text. It understands:
- Punctuation intensity ("good" vs "good!!!")
- Capitalization emphasis ("AMAZING")
- Negations ("not good")
- Emoji sentiment

**Streamlit**: Transforms Python scripts into interactive web applications without requiring HTML/CSS/JavaScript knowledge. Provides:
- Automatic UI generation
- Session state management
- File upload widgets
- Chart rendering

**Plotly**: Creates interactive, publication-quality graphs. Advantages:
- JavaScript-based rendering for smooth interactions
- Responsive and mobile-friendly
- Export capabilities
- Professional styling

### 📊 Analysis Methodologies

#### Emoji Analysis
Emojis are extracted character-by-character using the `emoji` library, which maintains a comprehensive database of Unicode emoji characters. Each emoji is counted, ranked, and attributed to specific users.

#### Word Frequency Analysis
**Process:**
1. Extract text from non-media, non-system messages
2. Convert to lowercase
3. Split into individual words using regex
4. Filter out stop words (common words like "the", "is", "a")
5. Apply minimum length filter
6. Count occurrences
7. Rank by frequency

#### Sentiment Scoring
VADER produces four scores for each message:
- **Positive**: Proportion of positive sentiment (0-1)
- **Neutral**: Proportion of neutral sentiment (0-1)
- **Negative**: Proportion of negative sentiment (0-1)
- **Compound**: Normalized weighted composite score (-1 to +1)

Classification logic:
- Compound ≥ 0.05: Positive
- Compound ≤ -0.05: Negative
- Otherwise: Neutral

#### Response Time Calculation
Messages are sorted chronologically. When consecutive messages are from different authors, the time difference is calculated. Only differences under 2 hours are considered "responses" to filter out conversations that resumed after long breaks.

###  Features in Detail

#### Feature 1: User Statistics Dashboard
Provides a comprehensive breakdown of messaging behavior:
- Message count per user with percentage distribution
- Average message length (helps identify verbose vs concise communicators)
- Total words and average words per message
- Media sharing frequency (photos, videos, documents)
- URL sharing patterns

**Use Cases:**
- Understand who dominates conversations
- Identify communication styles
- Track content sharing habits

#### Feature 2: Activity Timeline Analysis
Visualize conversation intensity over time:
- Daily view: See exact message counts per day
- Weekly view: Identify weekly patterns and trends
- Monthly view: Track long-term engagement changes
- Per-user breakdowns available for all time frames

**Use Cases:**
- Identify when relationships were most active
- Detect conversation peaks and valleys
- Correlate external events with messaging patterns

#### Feature 3: Temporal Pattern Detection
**Hourly Activity Heatmap:**
- Shows which hours of the day see most activity
- Identifies night owls vs early birds
- Reveals time zone differences in group chats

**Daily Activity Analysis:**
- Compares weekday vs weekend behavior
- Identifies routine messaging patterns
- Shows which days are most conversational

**Use Cases:**
- Optimize when to send important messages
- Understand availability patterns
- Detect lifestyle changes over time

#### Feature 4: Emoji Usage Analysis
Emojis reveal emotional expression and personality:
- Total emoji count across the conversation
- Ranking of most-used emojis
- Per-user emoji preferences
- Emoji diversity metrics

**Insights Provided:**
- Emotional expression styles
- Humor indicators (😂, 🤣)
- Affection patterns (❤️, 😊)
- Cultural differences in emoji usage

#### Feature 5: Word Cloud & Frequency Analysis
Visual representation of conversation topics:
- Generates beautiful word clouds
- Lists most common words with counts
- Filters out meaningless stop words
- Per-user vocabulary analysis

**Applications:**
- Identify main conversation topics
- Detect recurring themes
- Understand shared interests
- Track vocabulary evolution

#### Feature 6: Sentiment Analysis
Understand the emotional tone of conversations:
- Overall sentiment distribution (positive/neutral/negative)
- Per-user sentiment profiles
- Time-series sentiment tracking (planned feature)
- Compound sentiment scores

**Psychological Insights:**
- Detect generally positive or negative relationships
- Identify emotional support patterns
- Track mood changes over time
- Compare emotional expression between users

#### Feature 7: Response Time Analytics
Measure engagement and responsiveness:
- Average response time per user
- Median response time (less affected by outliers)
- Response time distribution
- Fast vs slow responder identification

**Relationship Insights:**
- Measure engagement levels
- Identify prioritization patterns
- Detect changes in responsiveness
- Compare mutual engagement

###  How to Use This Project

#### Method 1: Web Dashboard (Recommended for Most Users)

**Step 1: Start the Dashboard**
```bash
streamlit run src/whatsapp_analyzer/app.py
```
Or double-click `run_dashboard.bat` on Windows.

**Step 2: Export Your WhatsApp Chat**
- Open the chat in WhatsApp
- Tap menu (⋮ or contact name)
- Select "Export Chat"
- Choose "Without Media"
- Save the .txt file

**Step 3: Upload and Analyze**
- Drag the .txt file to the upload area
- Wait for parsing (usually 1-3 seconds)
- Explore the six analysis tabs
- Interact with visualizations
- Download charts as needed

#### Method 2: Python API (For Developers & Data Scientists)

**Basic Analysis:**
```python
from whatsapp_analyzer import ChatParser, ChatAnalyzer

# Load chat
parser = ChatParser('chat.txt')
df = parser.load_chat()

# Get basic info
info = parser.get_chat_info()
print(f"Total messages: {info['total_messages']}")
print(f"Participants: {info['participant_names']}")
print(f"Date range: {info['date_range']['start']} to {info['date_range']['end']}")

# Analyze
analyzer = ChatAnalyzer(df)
user_stats = analyzer.get_user_stats()
print(user_stats)
```

**Advanced Analysis:**
```python
# Emoji analysis
emoji_data = analyzer.analyze_emojis(top_n=20)
print(f"Total emojis used: {emoji_data['total_emojis']}")
for emoji, count in emoji_data['most_common'][:5]:
    print(f"{emoji}: {count} times")

# Sentiment analysis
sentiment = analyzer.get_sentiment_summary()
for user, scores in sentiment['per_user'].items():
    print(f"{user}: {scores['positive']} positive, {scores['negative']} negative")

# Response times
response_stats = analyzer.get_response_time_stats()
for user, stats in response_stats['per_user'].items():
    print(f"{user} average response: {stats['mean']:.1f} minutes")
```

**Custom Visualizations:**
```python
from whatsapp_analyzer import ChatVisualizer
import matplotlib.pyplot as plt

visualizer = ChatVisualizer()

# Create word cloud
word_data = analyzer.analyze_word_frequency(top_n=50)
wordcloud = visualizer.create_wordcloud(word_data, save_path='wordcloud.png')

# Plot activity timeline
timeline = analyzer.get_activity_timeline(freq='W')  # Weekly
fig = visualizer.plot_activity_timeline(timeline, interactive=False)
plt.show()

# Generate all visualizations
user_stats = analyzer.get_user_stats()
visualizer.plot_user_message_distribution(user_stats, save_path='distribution.png')

hourly = analyzer.get_hourly_activity()
visualizer.plot_hourly_activity(hourly, save_path='hourly.png')
```

###  Installation & Setup

**Prerequisites:**
- Python 3.9 or higher
- pip package manager
- 50MB free disk space

**Installation Steps:**

1. **Navigate to project directory:**
```bash
cd whatsapp-chat-analyzer
```

2. **Create virtual environment (recommended):**
```bash
python -m venv venv
```

3. **Activate virtual environment:**
```bash
# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

4. **Install dependencies:**
```bash
pip install -r requirements.txt
```

**Verify Installation:**
```bash
python -c "import whatsapp_analyzer; print('Installation successful!')"
```

## 📖 Usage

### Method 1: Interactive Dashboard (Recommended)

Launch the Streamlit dashboard:
```bash
streamlit run src/whatsapp_analyzer/app.py
```

Then:
1. Upload your WhatsApp chat export (.txt file)
2. Explore different analysis tabs
3. View interactive visualizations

### Method 2: Python API

```python
from whatsapp_analyzer import ChatParser, ChatAnalyzer, ChatVisualizer

# Parse chat file
parser = ChatParser('path/to/chat.txt')
df = parser.load_chat()

# Analyze chat
analyzer = ChatAnalyzer(df)
user_stats = analyzer.get_user_stats()
emoji_data = analyzer.analyze_emojis()
sentiment = analyzer.get_sentiment_summary()

# Visualize results
visualizer = ChatVisualizer()
fig = visualizer.plot_user_message_distribution(user_stats)
visualizer.create_wordcloud(analyzer.analyze_word_frequency())
```

### Method 3: Command Line Usage

```python
# Example script
from whatsapp_analyzer import ChatParser, ChatAnalyzer

parser = ChatParser('chat.txt')
df = parser.load_chat()
info = parser.get_chat_info()

print(f"Total messages: {info['total_messages']}")
print(f"Participants: {info['participant_names']}")
```

###  Example Output & Interpretation

**Sample User Statistics Output:**
```
author  total_messages  avg_message_length  total_words  media_messages  message_percentage
Alice   1,247          42.3                18,450       87              58.2%
Bob     895            51.7                15,320       65              41.8%
```

**Interpretation:**
- Alice sends more messages (58.2% of total) but with shorter average length
- Bob sends fewer but longer messages, suggesting different communication styles
- Alice shares slightly more media (87 vs 65)

**Sample Sentiment Analysis:**
```
Overall: 45% Positive, 48% Neutral, 7% Negative
Alice: Avg Compound Score: +0.34 (Generally positive)
Bob: Avg Compound Score: +0.28 (Slightly positive)
```

**Interpretation:**
- The conversation is predominantly positive
- Very low negative sentiment (7%) indicates a healthy interaction
- Both users maintain positive tone, with Alice slightly more positive

###  Project File Structure Explained

```
whatsapp-chat-analyzer/
├── src/                          # Source code directory
│   └── whatsapp_analyzer/        # Main package
│       ├── __init__.py           # Package initialization, exports main classes
│       ├── parser.py             # ChatParser class - handles file reading & parsing
│       ├── analyzer.py           # ChatAnalyzer class - performs all analysis
│       ├── visualizer.py         # ChatVisualizer class - creates charts & graphs
│       └── app.py                # Streamlit dashboard application
│
├── tests/                        # Unit tests directory
│   ├── __init__.py
│   ├── test_parser.py            # Tests for parser functionality
│   └── test_analyzer.py          # Tests for analysis functions
│
├── data/                         # Data directory
│   └── sample/                   # Sample data for testing
│       └── sample_chat.txt       # Example WhatsApp export file
│
├── docs/                         # Documentation (future expansion)
│
├── notebooks/                    # Jupyter notebooks (future expansion)
│
├── requirements.txt              # Python dependencies list
├── pyproject.toml                # Modern Python project configuration
├── .gitignore                    # Git ignore rules
├── LICENSE                       # MIT License
├── README.md                     # This file - project documentation
├── QUICKSTART.md                 # Quick setup guide
└── run_dashboard.bat             # Windows batch script to launch dashboard
```

**Key Files Explained:**

- **parser.py**: Contains regex patterns for different WhatsApp formats, datetime parsing logic, and DataFrame construction
- **analyzer.py**: Implements all statistical analysis methods using pandas operations
- **visualizer.py**: Uses matplotlib, seaborn, and plotly to create various chart types
- **app.py**: Streamlit application with file upload, tabs, and interactive widgets
- **requirements.txt**: Lists all Python packages needed (pandas, streamlit, etc.)
- **pyproject.toml**: Modern Python packaging standard with metadata and tool configurations

###  Testing & Quality Assurance

**Running Tests:**
```bash
# Run all tests
pytest tests/ -v

# Run with coverage report
pytest tests/ --cov=src/whatsapp_analyzer --cov-report=html

# Run specific test file
pytest tests/test_parser.py -v

# Run specific test
pytest tests/test_parser.py::TestChatParser::test_match_android_pattern -v
```

**What's Tested:**

**Parser Tests:**
- Message pattern recognition (Android/iOS formats)
- Multiline message handling
- Media message detection
- System message identification
- Datetime parsing accuracy
- DataFrame structure validation

**Analyzer Tests:**
- User statistics calculation
- Activity timeline generation
- Emoji extraction and counting
- Word frequency analysis
- Sentiment scoring
- Response time calculations

**Test Coverage:**
Current test suite covers approximately 70% of codebase, focusing on critical parsing and analysis functions.

###  Configuration & Customization

**Customizing Analysis Parameters:**

```python
# Adjust word frequency analysis
word_data = analyzer.analyze_word_frequency(
    top_n=100,          # Return top 100 words instead of default 30
    min_length=5        # Only count words 5+ characters long
)

# Change activity timeline granularity
timeline_daily = analyzer.get_activity_timeline(freq='D')     # Daily
timeline_weekly = analyzer.get_activity_timeline(freq='W')    # Weekly  
timeline_monthly = analyzer.get_activity_timeline(freq='M')   # Monthly

# Adjust emoji analysis depth
emoji_data = analyzer.analyze_emojis(top_n=50)  # Get top 50 emojis
```

**Customizing Visualizations:**

```python
# Change matplotlib style
visualizer = ChatVisualizer(style='ggplot')  # Use ggplot style

# Customize word cloud
wordcloud = visualizer.create_wordcloud(
    word_freq=word_data,
    max_words=200,              # Include 200 words
    save_path='custom_wc.png'
)

# Save charts to files
visualizer.plot_user_message_distribution(
    user_stats, 
    save_path='charts/user_dist.png'
)
```

**Adding Custom Stop Words:**

Edit `analyzer.py` line ~194 to add your own stop words:
```python
stop_words = {
    'the', 'is', 'at', ...,  # existing words
    'custom_word1', 'custom_word2'  # your additions
}
```

###  Exporting WhatsApp Chats (Detailed)

**Android Devices:**
1. Open WhatsApp application
2. Navigate to the chat you want to analyze
3. Tap the three vertical dots (⋮) in the top-right corner
4. Select "More" from the dropdown menu
5. Tap "Export chat"
6. When prompted, select "Without media" (media files are not needed for text analysis)
7. Choose your preferred sharing method (Email, Drive, etc.)
8. Save the `.txt` file to your device or computer

**iOS Devices (iPhone/iPad):**
1. Open WhatsApp application
2. Navigate to the chat you want to analyze
3. Tap the contact or group name at the top of the screen
4. Scroll down in the Contact/Group Info screen
5. Tap "Export Chat"
6. Select "Without Media" when prompted
7. Choose sharing method (AirDrop, Email, Save to Files, etc.)
8. Save the `.txt` file to your computer

**Important Notes:**
- Always choose "Without Media" - this project analyzes text only
- Exported files are named like: "WhatsApp Chat with Contact Name.txt"
- Export size limits: ~40,000 messages on iOS, ~100,000 on Android
- For very large chats, consider analyzing in chunks
- The export includes timestamps, usernames, and message content

**Sample Export Format:**
```
12/25/2023, 10:30 AM - Alice: Hey! How are you?
12/25/2023, 10:32 AM - Bob: I'm great! How about you?
12/25/2023, 10:35 AM - Alice: Doing well, thanks! 😊
```

### ⚠️ Privacy & Security

**Data Privacy Principles:**

1. **Local Processing**: All analysis happens on your local machine. No data is transmitted to external servers.

2. **No Cloud Storage**: Unless you explicitly save results, nothing is stored in the cloud.

3. **Temporary Files**: The dashboard creates temporary files during analysis, which are automatically deleted when you close the session.

4. **Anonymization**: When sharing results, consider removing or anonymizing names:
   ```python
   # Replace names before analysis
   df['author'] = df['author'].replace({
       'Real Name 1': 'Person A',
       'Real Name 2': 'Person B'
   })
   ```

5. **Consent**: Only analyze chats where all participants have consented to the analysis.

**Security Best Practices:**
- Don't share your raw chat export files publicly
- Delete export files after analysis if they contain sensitive information
- Be cautious when sharing screenshots of analysis results
- Use virtual environments to isolate dependencies

###  Troubleshooting Common Issues

**Problem: "FileNotFoundError" or chat won't load**
- Solution: Ensure file path is correct and uses forward slashes or escaped backslashes
- Check file encoding (should be UTF-8)
- Verify the file is a WhatsApp export, not a screenshot or modified file

**Problem: "ValueError: Could not parse datetime"**
- Solution: The export format may not be recognized
- Check if your WhatsApp uses a different date format
- Contact support or modify `parser.py` datetime formats

**Problem: Dashboard shows "No data" or empty charts**
- Solution: Verify the chat has actual messages (not just system notifications)
- Check if messages are being filtered out as system messages
- Ensure dates are parsing correctly

**Problem: Emoji analysis shows zero emojis**
- Solution: Update the `emoji` package: `pip install --upgrade emoji`
- Verify your chat actually contains emoji characters

**Problem: High memory usage with large chats**
- Solution: Process in chunks or use sampling
- Close other applications to free up RAM
- Consider analyzing shorter time periods

**Problem: Streamlit dashboard won't start**
- Solution: Check if port 8501 is already in use
- Try: `streamlit run src/whatsapp_analyzer/app.py --server.port 8502`
- Ensure all dependencies are installed: `pip install -r requirements.txt`

###  Performance Considerations

**Optimal Performance:**
- Chat size: 100 - 10,000 messages works best
- Processing time: ~1-3 seconds for typical chats
- Memory usage: ~100-200 MB for moderate chats

**Large Chat Handling:**
- Chats with 50,000+ messages may take 10-30 seconds
- Consider sampling: analyze every Nth message
- Use monthly aggregation instead of daily for timelines

**Optimization Tips:**
```python
# Sample large datasets
df_sample = df.sample(n=10000)  # Analyze 10,000 random messages

# Focus on recent messages
df_recent = df[df['datetime'] > '2024-01-01']

# Skip computationally expensive analyses
# sentiment = analyzer.get_sentiment_summary()  # Skip if not needed
```

### User Statistics
```python
analyzer = ChatAnalyzer(df)
stats = analyzer.get_user_stats()
print(stats)
```

Output:
```
   author  total_messages  avg_message_length  total_words  media_messages
0  Alice              120               45.2          850              15
1  Bob                 98               52.1          720              12
```

### Emoji Analysis
```python
emoji_data = analyzer.analyze_emojis(top_n=10)
print(f"Total emojis: {emoji_data['total_emojis']}")
print(f"Most common: {emoji_data['most_common'][:5]}")
```

### Sentiment Analysis
```python
sentiment = analyzer.get_sentiment_summary()
print(f"Positive: {sentiment['overall']['positive']}")
print(f"Neutral: {sentiment['overall']['neutral']}")
print(f"Negative: {sentiment['overall']['negative']}")
```

##  Project Structure

```
whatsapp-chat-analyzer/
├── src/
│   └── whatsapp_analyzer/
│       ├── __init__.py
│       ├── parser.py          # Chat parsing logic
│       ├── analyzer.py        # Analysis algorithms
│       ├── visualizer.py      # Visualization functions
│       └── app.py            # Streamlit dashboard
├── tests/
│   ├── __init__.py
│   ├── test_parser.py
│   └── test_analyzer.py
├── data/
│   └── sample/
│       └── sample_chat.txt
├── docs/
├── notebooks/                 # Jupyter notebooks for exploration
├── requirements.txt
├── pyproject.toml
├── .gitignore
└── README.md
```

##  Configuration

### Analysis Settings

Customize analysis parameters in your code:

```python
# Word frequency with custom parameters
word_data = analyzer.analyze_word_frequency(
    top_n=50,           # Number of top words
    min_length=4        # Minimum word length
)

# Activity timeline with different frequencies
timeline = analyzer.get_activity_timeline(
    freq='W'  # 'D' for daily, 'W' for weekly, 'M' for monthly
)
```

### Visualization Settings

```python
# Initialize visualizer with custom style
visualizer = ChatVisualizer(style='seaborn-v0_8-darkgrid')

# Create word cloud with custom parameters
wordcloud = visualizer.create_wordcloud(
    word_freq=word_data,
    max_words=150,
    save_path='wordcloud.png'
)
```

### 💡 Use Cases & Applications

**Personal Relationships:**
- Track communication patterns with partners, friends, family
- Identify when relationships were most active
- Understand emotional dynamics over time
- Celebrate conversation milestones

**Professional Research:**
- Communication studies and linguistics research
- Social psychology experiments
- Data science portfolio projects
- Natural language processing demonstrations

**Business Analysis:**
- Customer support chat analysis
- Team communication patterns
- Response time optimization
- Customer sentiment tracking

**Educational:**
- Teaching data analysis concepts
- Demonstrating NLP techniques
- Python programming examples
- Data visualization tutorials

###  Technology Stack Deep Dive

**Core Dependencies:**

| Library | Version | Purpose | Why This Choice? |
|---------|---------|---------|------------------|
| pandas | 2.0+ | Data manipulation | Industry standard, powerful DataFrame operations |
| numpy | 1.24+ | Numerical computing | Fast array operations, pandas dependency |
| matplotlib | 3.7+ | Static visualization | Mature, highly customizable plotting |
| seaborn | 0.13+ | Statistical visualization | Beautiful defaults, built on matplotlib |
| plotly | 5.18+ | Interactive visualization | Modern, web-ready interactive charts |
| streamlit | 1.29+ | Web dashboard | Rapid prototyping, Python-native |
| emoji | 2.10+ | Emoji processing | Comprehensive emoji database |
| vaderSentiment | 3.3+ | Sentiment analysis | Optimized for social media text |
| wordcloud | 1.9+ | Word cloud generation | Simple API, attractive output |

**Why These Technologies?**

- **pandas**: Unmatched for tabular data analysis in Python
- **Streamlit**: Fastest way to build data apps without frontend code
- **VADER**: Specifically designed for social media sentiment (better than generic models)
- **Plotly**: Enables interactivity without JavaScript knowledge

###  Additional Resources

**Learning Materials:**
- [QUICKSTART.md](QUICKSTART.md) - Quick setup guide
- `data/sample/sample_chat.txt` - Example chat for testing
- Unit tests in `tests/` - Code usage examples

**External Documentation:**
- [pandas Documentation](https://pandas.pydata.org/docs/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [VADER Sentiment Analysis Paper](https://github.com/cjhutto/vaderSentiment)
- [Plotly Python Documentation](https://plotly.com/python/)

**Related Projects:**
- [WA-ChatAnalyzer](https://github.com/pankajcr7/WA-ChatAnalyzer) - Similar project
- [WhatsApp-Chat-Analyzer-Pro](https://github.com/harshbg/WhatsApp-Chat-Analyzer-Pro) - Alternative implementation

### ❓ FAQ (Frequently Asked Questions)

**Q: Can I analyze group chats?**
A: Yes! The tool works with both individual and group chats. Group chats will show statistics for all participants.

**Q: Does this work with WhatsApp Business?**
A: Yes, WhatsApp Business exports use the same format.

**Q: Can I compare multiple chats?**
A: Not directly in v0.1.0, but you can run separate analyses and compare manually. Multi-chat comparison is planned for future versions.

**Q: Will this work on my phone?**
A: The dashboard is best viewed on a computer. You can export chats from your phone and analyze on a computer.

**Q: How accurate is the sentiment analysis?**
A: VADER is ~85% accurate on social media text. It's good for general trends but may misinterpret sarcasm or context-dependent phrases.

**Q: Can I use this for languages other than English?**
A: Currently optimized for English. Other languages may work partially (emoji/activity analysis), but sentiment and word frequency will be less accurate.

**Q: Is my data shared or uploaded anywhere?**
A: No! All processing is 100% local. Your chat data never leaves your computer.

**Q: Can I export the analysis results?**
A: Charts can be saved as PNG/HTML files. You can also access the DataFrames directly via the Python API for custom exports.

### 🤝 Contributing

Contributions are welcome! This project can be improved in many ways:

**How to Contribute:**

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/YourFeature`
3. **Make your changes** with clear, commented code
4. **Add tests** for new functionality
5. **Update documentation** if needed
6. **Commit with descriptive messages**: `git commit -m 'Add: feature description'`
7. **Push to your fork**: `git push origin feature/YourFeature`
8. **Open a Pull Request** with detailed description

**Contribution Ideas:**
- Add support for more chat platforms (Telegram, Discord, Signal)
- Implement additional NLP features (topic modeling, named entity recognition)
- Create Jupyter notebook tutorials
- Add more visualization types
- Improve test coverage
- Optimize performance for large chats
- Add internationalization support
- Create video tutorials

**Code Style:**
- Follow PEP 8 guidelines
- Use type hints where possible
- Write docstrings for all functions
- Keep functions focused and modular

###  License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for full details.

**What this means:**
-  Commercial use allowed
-  Modification allowed
-  Distribution allowed
-  Private use allowed
-  License and copyright notice required
-  No liability or warranty provided

###  Acknowledgments

This project wouldn't be possible without these amazing open-source libraries:

- **pandas** (BSD-3-Clause) - The backbone of data manipulation
- **matplotlib** (PSF License) - Foundational visualization library
- **seaborn** (BSD-3-Clause) - Beautiful statistical visualizations
- **plotly** (MIT) - Interactive, publication-quality graphs
- **streamlit** (Apache 2.0) - Rapid data app development
- **VADER** (MIT) - Social media sentiment analysis
- **emoji** (BSD License) - Unicode emoji support
- **wordcloud** (MIT) - Text visualization
- **textblob** (MIT) - Text processing

Special thanks to the open-source community for making data science accessible to everyone.

###  Roadmap & Future Enhancements

**Version 0.2.0 (Planned)**
- [ ] Multi-chat comparison feature
- [ ] PDF export of analysis reports
- [ ] Custom date range filtering
- [ ] Advanced filtering options (exclude users, keywords, etc.)
- [ ] Time-series sentiment analysis
- [ ] Conversation topic detection

**Version 0.3.0 (Planned)**
- [ ] Telegram export support
- [ ] Discord export support
- [ ] Named entity recognition
- [ ] Keyword extraction
- [ ] Network graph visualizations
- [ ] Export to Excel with multiple sheets

**Version 1.0.0 (Vision)**
- [ ] Real-time chat monitoring
- [ ] Machine learning predictions
- [ ] Multi-language support
- [ ] Advanced NLP (topic modeling, summarization)
- [ ] API for programmatic access
- [ ] Plugin system for custom analyzers

**Community Requests:**
- [ ] Dark mode for dashboard
- [ ] Custom color schemes
- [ ] Comparison with anonymized global statistics
- [ ] Relationship score calculator

###  Version History

**v0.1.0** (February 2024) - *Initial Release*

*Core Features:*
- WhatsApp chat parser supporting Android & iOS formats
- Comprehensive user statistics
- Activity timeline analysis (daily/weekly/monthly)
- Hourly and daily activity heatmaps
- Emoji usage analysis with per-user breakdowns
- Word frequency analysis with stop-word filtering
- Word cloud generation
- VADER-based sentiment analysis
- Response time calculations
- Interactive Streamlit dashboard
- Static and interactive visualizations
- Unit tests with pytest
- Sample data for testing
- Comprehensive documentation

*Technologies:*
- Python 3.9+
- pandas, numpy, matplotlib, seaborn, plotly
- streamlit, emoji, vaderSentiment, wordcloud

###  Support & Contact

**Need Help?**
-  Report bugs via GitHub Issues
-  Request features via GitHub Issues
-  Ask questions via GitHub Discussions
-  Read [QUICKSTART.md](QUICKSTART.md) for quick setup

**Found a Bug?**
Please include:
1. Your operating system and Python version
2. Steps to reproduce the issue
3. Sample chat file (anonymized) if possible
4. Error message or unexpected behavior description

---

<div align="center">

## ⭐ If you find this project useful, please consider giving it a star!


</div>

---

**© 2026 WhatsApp Chat Analyzer Project** | Licensed under MIT License
