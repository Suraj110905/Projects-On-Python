"""Unit tests for ChatAnalyzer module."""

import pytest
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from whatsapp_analyzer.parser import ChatParser
from whatsapp_analyzer.analyzer import ChatAnalyzer


class TestChatAnalyzer:
    """Test cases for ChatAnalyzer class."""
    
    @pytest.fixture
    def sample_analyzer(self):
        """Create analyzer with sample data."""
        sample_path = Path(__file__).parent.parent / 'data' / 'sample' / 'sample_chat.txt'
        
        if not sample_path.exists():
            pytest.skip("Sample chat file not found")
        
        parser = ChatParser(str(sample_path))
        df = parser.load_chat()
        return ChatAnalyzer(df)
    
    def test_analyzer_initialization(self, sample_analyzer):
        """Test analyzer initialization."""
        assert sample_analyzer.df is not None
        assert len(sample_analyzer.df) > 0
        assert 'hour' in sample_analyzer.df.columns
        assert 'day_of_week' in sample_analyzer.df.columns
        assert 'emoji_count' in sample_analyzer.df.columns
    
    def test_get_user_stats(self, sample_analyzer):
        """Test user statistics generation."""
        stats = sample_analyzer.get_user_stats()
        
        assert stats is not None
        assert len(stats) > 0
        assert 'author' in stats.columns
        assert 'total_messages' in stats.columns
        assert 'avg_message_length' in stats.columns
        assert stats['total_messages'].sum() > 0
    
    def test_get_activity_timeline(self, sample_analyzer):
        """Test activity timeline generation."""
        timeline = sample_analyzer.get_activity_timeline(freq='D')
        
        assert timeline is not None
        assert len(timeline) > 0
        assert 'datetime' in timeline.columns
        assert 'message_count' in timeline.columns
    
    def test_get_hourly_activity(self, sample_analyzer):
        """Test hourly activity analysis."""
        hourly = sample_analyzer.get_hourly_activity()
        
        assert hourly is not None
        assert 'hour' in hourly.columns
        assert 'message_count' in hourly.columns
    
    def test_get_daily_activity(self, sample_analyzer):
        """Test daily activity analysis."""
        daily = sample_analyzer.get_daily_activity()
        
        assert daily is not None
        assert 'day_of_week' in daily.columns
        assert 'message_count' in daily.columns
    
    def test_analyze_emojis(self, sample_analyzer):
        """Test emoji analysis."""
        emoji_data = sample_analyzer.analyze_emojis(top_n=10)
        
        assert emoji_data is not None
        assert 'total_emojis' in emoji_data
        assert 'unique_emojis' in emoji_data
        assert 'most_common' in emoji_data
        assert 'per_user' in emoji_data
    
    def test_analyze_word_frequency(self, sample_analyzer):
        """Test word frequency analysis."""
        word_data = sample_analyzer.analyze_word_frequency(top_n=20, min_length=3)
        
        assert word_data is not None
        assert 'total_words' in word_data
        assert 'unique_words' in word_data
        assert 'most_common' in word_data
        assert 'per_user' in word_data
    
    def test_get_sentiment_summary(self, sample_analyzer):
        """Test sentiment analysis."""
        sentiment = sample_analyzer.get_sentiment_summary()
        
        assert sentiment is not None
        assert 'overall' in sentiment
        assert 'per_user' in sentiment
        assert 'positive' in sentiment['overall']
        assert 'neutral' in sentiment['overall']
        assert 'negative' in sentiment['overall']
    
    def test_calculate_response_times(self, sample_analyzer):
        """Test response time calculation."""
        response_times = sample_analyzer.calculate_response_times()
        
        # May be empty depending on chat structure
        assert response_times is not None
        if not response_times.empty:
            assert 'from_author' in response_times.columns
            assert 'to_author' in response_times.columns
            assert 'response_time_minutes' in response_times.columns


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
