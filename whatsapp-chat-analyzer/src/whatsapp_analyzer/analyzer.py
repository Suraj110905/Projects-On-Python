"""WhatsApp Chat Analyzer - Comprehensive analysis of chat data."""

import re
from typing import Dict, List, Optional, Tuple
from collections import Counter
import pandas as pd
import numpy as np
import emoji
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


class ChatAnalyzer:
    """Analyze WhatsApp chat data with various metrics and insights."""
    
    def __init__(self, dataframe: pd.DataFrame):
        """Initialize analyzer with parsed chat data.
        
        Args:
            dataframe: DataFrame from ChatParser containing chat messages
        """
        self.df = dataframe.copy()
        self.sentiment_analyzer = SentimentIntensityAnalyzer()
        self._prepare_data()
        
    def _prepare_data(self):
        """Prepare and enrich data with additional features."""
        if self.df.empty:
            return
            
        # Add time-based features
        self.df['date'] = self.df['datetime'].dt.date
        self.df['time'] = self.df['datetime'].dt.time
        self.df['hour'] = self.df['datetime'].dt.hour
        self.df['day_of_week'] = self.df['datetime'].dt.day_name()
        self.df['month'] = self.df['datetime'].dt.month
        self.df['year'] = self.df['datetime'].dt.year
        self.df['day_name'] = self.df['datetime'].dt.day_name()
        
        # Add message length
        self.df['message_length'] = self.df['message'].str.len()
        self.df['word_count'] = self.df['message'].apply(lambda x: len(str(x).split()))
        
        # Extract URLs
        self.df['has_url'] = self.df['message'].apply(self._contains_url)
        
        # Extract emojis
        self.df['emoji_count'] = self.df['message'].apply(self._count_emojis)
        self.df['emojis'] = self.df['message'].apply(self._extract_emojis)
        
    def _contains_url(self, text: str) -> bool:
        """Check if text contains URL."""
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        return bool(re.search(url_pattern, text))
    
    def _count_emojis(self, text: str) -> int:
        """Count emojis in text."""
        return len([c for c in text if c in emoji.EMOJI_DATA])
    
    def _extract_emojis(self, text: str) -> List[str]:
        """Extract all emojis from text."""
        return [c for c in text if c in emoji.EMOJI_DATA]
    
    def get_user_stats(self) -> pd.DataFrame:
        """Get comprehensive statistics for each user.
        
        Returns:
            DataFrame with per-user statistics
        """
        user_messages = self.df[~self.df['is_system']].groupby('author').agg({
            'message': 'count',
            'message_length': ['mean', 'sum'],
            'word_count': ['mean', 'sum'],
            'is_media': 'sum',
            'has_url': 'sum',
            'emoji_count': 'sum'
        }).reset_index()
        
        user_messages.columns = [
            'author', 'total_messages', 'avg_message_length', 'total_chars',
            'avg_words_per_message', 'total_words', 'media_messages', 
            'urls_shared', 'total_emojis'
        ]
        
        # Calculate percentages
        total_msgs = user_messages['total_messages'].sum()
        user_messages['message_percentage'] = (
            user_messages['total_messages'] / total_msgs * 100
        ).round(2)
        
        return user_messages.sort_values('total_messages', ascending=False)
    
    def get_activity_timeline(self, freq: str = 'D') -> pd.DataFrame:
        """Get message activity over time.
        
        Args:
            freq: Frequency for grouping ('D' for daily, 'W' for weekly, 'M' for monthly)
            
        Returns:
            DataFrame with message counts over time
        """
        timeline = self.df[~self.df['is_system']].groupby([
            pd.Grouper(key='datetime', freq=freq),
            'author'
        ]).size().reset_index(name='message_count')
        
        return timeline
    
    def get_hourly_activity(self) -> pd.DataFrame:
        """Get message activity by hour of day.
        
        Returns:
            DataFrame with hourly message distribution
        """
        hourly = self.df[~self.df['is_system']].groupby(['hour', 'author']).size()
        hourly = hourly.reset_index(name='message_count')
        
        return hourly
    
    def get_daily_activity(self) -> pd.DataFrame:
        """Get message activity by day of week.
        
        Returns:
            DataFrame with daily message distribution
        """
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        daily = self.df[~self.df['is_system']].groupby(['day_of_week', 'author']).size()
        daily = daily.reset_index(name='message_count')
        daily['day_of_week'] = pd.Categorical(daily['day_of_week'], categories=day_order, ordered=True)
        daily = daily.sort_values('day_of_week')
        
        return daily
    
    def get_most_active_days(self, top_n: int = 10) -> pd.DataFrame:
        """Get the most active days by message count.
        
        Args:
            top_n: Number of top days to return
            
        Returns:
            DataFrame with most active days
        """
        active_days = self.df[~self.df['is_system']].groupby('date').agg({
            'message': 'count',
            'author': lambda x: x.value_counts().to_dict()
        }).reset_index()
        
        active_days.columns = ['date', 'message_count', 'author_breakdown']
        active_days = active_days.sort_values('message_count', ascending=False).head(top_n)
        
        return active_days
    
    def analyze_emojis(self, top_n: int = 20) -> Dict:
        """Analyze emoji usage in the chat.
        
        Args:
            top_n: Number of top emojis to return
            
        Returns:
            Dictionary with emoji statistics
        """
        all_emojis = []
        for emoji_list in self.df['emojis']:
            all_emojis.extend(emoji_list)
            
        emoji_counter = Counter(all_emojis)
        
        # Per-user emoji analysis
        user_emojis = {}
        for author in self.df['author'].unique():
            user_df = self.df[self.df['author'] == author]
            user_emoji_list = []
            for emoji_list in user_df['emojis']:
                user_emoji_list.extend(emoji_list)
            user_emojis[author] = Counter(user_emoji_list).most_common(10)
        
        return {
            'total_emojis': len(all_emojis),
            'unique_emojis': len(emoji_counter),
            'most_common': emoji_counter.most_common(top_n),
            'per_user': user_emojis
        }
    
    def analyze_word_frequency(self, top_n: int = 30, min_length: int = 3) -> Dict:
        """Analyze word frequency in messages.
        
        Args:
            top_n: Number of top words to return
            min_length: Minimum word length to consider
            
        Returns:
            Dictionary with word frequency statistics
        """
        # Common stop words to filter
        stop_words = {
            'the', 'is', 'at', 'which', 'on', 'and', 'a', 'to', 'in', 'was',
            'it', 'of', 'for', 'as', 'with', 'be', 'are', 'by', 'this', 'that',
            'from', 'or', 'have', 'an', 'not', 'but', 'what', 'all', 'were',
            'when', 'we', 'there', 'can', 'been', 'has', 'if', 'more', 'her',
            'his', 'they', 'you', 'me', 'my', 'i', 'im', 'dont', 'didnt'
        }
        
        # Extract words from non-media, non-system messages
        text_messages = self.df[
            (~self.df['is_media']) & (~self.df['is_system'])
        ]['message']
        
        all_words = []
        for message in text_messages:
            words = re.findall(r'\b[a-zA-Z]+\b', message.lower())
            words = [w for w in words if len(w) >= min_length and w not in stop_words]
            all_words.extend(words)
        
        word_counter = Counter(all_words)
        
        # Per-user word analysis
        user_words = {}
        for author in self.df['author'].unique():
            user_messages = self.df[
                (self.df['author'] == author) & 
                (~self.df['is_media']) & 
                (~self.df['is_system'])
            ]['message']
            
            user_word_list = []
            for message in user_messages:
                words = re.findall(r'\b[a-zA-Z]+\b', message.lower())
                words = [w for w in words if len(w) >= min_length and w not in stop_words]
                user_word_list.extend(words)
            
            user_words[author] = Counter(user_word_list).most_common(top_n)
        
        return {
            'total_words': len(all_words),
            'unique_words': len(word_counter),
            'most_common': word_counter.most_common(top_n),
            'per_user': user_words
        }
    
    def analyze_sentiment(self) -> pd.DataFrame:
        """Analyze sentiment of messages using VADER.
        
        Returns:
            DataFrame with sentiment scores
        """
        text_messages = self.df[
            (~self.df['is_media']) & (~self.df['is_system'])
        ].copy()
        
        sentiments = text_messages['message'].apply(
            lambda x: self.sentiment_analyzer.polarity_scores(str(x))
        )
        
        text_messages['sentiment_negative'] = sentiments.apply(lambda x: x['neg'])
        text_messages['sentiment_neutral'] = sentiments.apply(lambda x: x['neu'])
        text_messages['sentiment_positive'] = sentiments.apply(lambda x: x['pos'])
        text_messages['sentiment_compound'] = sentiments.apply(lambda x: x['compound'])
        
        # Classify sentiment
        text_messages['sentiment_label'] = text_messages['sentiment_compound'].apply(
            lambda x: 'positive' if x >= 0.05 else ('negative' if x <= -0.05 else 'neutral')
        )
        
        return text_messages
    
    def get_sentiment_summary(self) -> Dict:
        """Get summary of sentiment analysis.
        
        Returns:
            Dictionary with sentiment statistics
        """
        sentiment_df = self.analyze_sentiment()
        
        overall_sentiment = {
            'positive': (sentiment_df['sentiment_label'] == 'positive').sum(),
            'neutral': (sentiment_df['sentiment_label'] == 'neutral').sum(),
            'negative': (sentiment_df['sentiment_label'] == 'negative').sum(),
            'avg_compound': sentiment_df['sentiment_compound'].mean()
        }
        
        # Per-user sentiment
        user_sentiment = {}
        for author in sentiment_df['author'].unique():
            user_df = sentiment_df[sentiment_df['author'] == author]
            user_sentiment[author] = {
                'positive': (user_df['sentiment_label'] == 'positive').sum(),
                'neutral': (user_df['sentiment_label'] == 'neutral').sum(),
                'negative': (user_df['sentiment_label'] == 'negative').sum(),
                'avg_compound': user_df['sentiment_compound'].mean()
            }
        
        return {
            'overall': overall_sentiment,
            'per_user': user_sentiment
        }
    
    def calculate_response_times(self) -> pd.DataFrame:
        """Calculate response times between messages.
        
        Returns:
            DataFrame with response time statistics
        """
        response_times = []
        
        # Sort by datetime
        sorted_df = self.df[~self.df['is_system']].sort_values('datetime')
        
        for i in range(1, len(sorted_df)):
            prev_msg = sorted_df.iloc[i-1]
            curr_msg = sorted_df.iloc[i]
            
            # Only count if different authors (response)
            if prev_msg['author'] != curr_msg['author']:
                time_diff = (curr_msg['datetime'] - prev_msg['datetime']).total_seconds() / 60
                
                # Only consider responses within 2 hours as actual responses
                if time_diff <= 120:
                    response_times.append({
                        'from_author': prev_msg['author'],
                        'to_author': curr_msg['author'],
                        'response_time_minutes': time_diff
                    })
        
        if not response_times:
            return pd.DataFrame()
            
        return pd.DataFrame(response_times)
    
    def get_response_time_stats(self) -> Dict:
        """Get response time statistics.
        
        Returns:
            Dictionary with response time metrics
        """
        response_df = self.calculate_response_times()
        
        if response_df.empty:
            return {}
        
        stats = {
            'overall': {
                'mean': response_df['response_time_minutes'].mean(),
                'median': response_df['response_time_minutes'].median(),
                'std': response_df['response_time_minutes'].std()
            }
        }
        
        # Per-user stats (who they respond to)
        user_stats = {}
        for author in response_df['to_author'].unique():
            user_responses = response_df[response_df['to_author'] == author]
            user_stats[author] = {
                'mean': user_responses['response_time_minutes'].mean(),
                'median': user_responses['response_time_minutes'].median(),
                'total_responses': len(user_responses)
            }
        
        stats['per_user'] = user_stats
        
        return stats
