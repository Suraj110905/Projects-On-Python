"""Group Chat Analyzer - Advanced analysis specifically for group conversations."""

import re
from typing import Dict, List, Tuple, Optional
from collections import Counter, defaultdict
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


class GroupChatAnalyzer:
    """Analyze group chat dynamics with interaction patterns and topic detection."""
    
    def __init__(self, dataframe: pd.DataFrame):
        """Initialize group analyzer with parsed chat data.
        
        Args:
            dataframe: DataFrame from ChatParser containing chat messages
        """
        self.df = dataframe.copy()
        self.is_group = len(self.df['author'].unique()) > 2
        
        # Add message_length if not present (needed for dominance score)
        if 'message_length' not in self.df.columns:
            self.df['message_length'] = self.df['message'].str.len()
        
        if not self.is_group:
            print("Note: This appears to be a one-on-one chat. Some group features may not be meaningful.")
    
    def get_interaction_matrix(self) -> pd.DataFrame:
        """Create an interaction matrix showing who responds to whom.
        
        Returns:
            DataFrame with interaction counts between users
        """
        # Sort by datetime
        sorted_df = self.df[~self.df['is_system']].sort_values('datetime').reset_index(drop=True)
        
        # Track interactions (who responds to whom)
        interactions = defaultdict(lambda: defaultdict(int))
        
        for i in range(1, len(sorted_df)):
            prev_author = sorted_df.iloc[i-1]['author']
            curr_author = sorted_df.iloc[i]['author']
            
            # If different authors within reasonable time (30 minutes)
            time_diff = (sorted_df.iloc[i]['datetime'] - sorted_df.iloc[i-1]['datetime']).total_seconds() / 60
            
            if prev_author != curr_author and time_diff <= 30:
                interactions[curr_author][prev_author] += 1
        
        # Convert to DataFrame
        authors = sorted(self.df['author'].unique())
        matrix = pd.DataFrame(0, index=authors, columns=authors)
        
        for responder, responded_to in interactions.items():
            for original_author, count in responded_to.items():
                if responder in matrix.index and original_author in matrix.columns:
                    matrix.loc[responder, original_author] = count
        
        return matrix
    
    def get_conversation_pairs(self, min_interactions: int = 5) -> List[Tuple[str, str, int]]:
        """Identify pairs of users who interact most frequently.
        
        Args:
            min_interactions: Minimum interactions to include a pair
            
        Returns:
            List of (user1, user2, interaction_count) tuples sorted by count
        """
        matrix = self.get_interaction_matrix()
        pairs = []
        
        authors = list(matrix.index)
        for i, user1 in enumerate(authors):
            for user2 in authors[i+1:]:
                # Bidirectional interaction count
                count = matrix.loc[user1, user2] + matrix.loc[user2, user1]
                if count >= min_interactions:
                    pairs.append((user1, user2, count))
        
        return sorted(pairs, key=lambda x: x[2], reverse=True)
    
    def get_reply_patterns(self) -> pd.DataFrame:
        """Analyze reply patterns - who responds fastest to whom.
        
        Returns:
            DataFrame with average response times between user pairs
        """
        sorted_df = self.df[~self.df['is_system']].sort_values('datetime').reset_index(drop=True)
        
        reply_times = defaultdict(list)
        
        for i in range(1, len(sorted_df)):
            prev_author = sorted_df.iloc[i-1]['author']
            curr_author = sorted_df.iloc[i]['author']
            
            if prev_author != curr_author:
                time_diff = (sorted_df.iloc[i]['datetime'] - sorted_df.iloc[i-1]['datetime']).total_seconds() / 60
                
                if time_diff <= 60:  # Within 1 hour
                    reply_times[(curr_author, prev_author)].append(time_diff)
        
        # Calculate statistics
        results = []
        for (responder, original), times in reply_times.items():
            if len(times) >= 3:  # At least 3 interactions
                results.append({
                    'responder': responder,
                    'responds_to': original,
                    'avg_response_time': np.mean(times),
                    'median_response_time': np.median(times),
                    'total_responses': len(times)
                })
        
        if not results:
            return pd.DataFrame()
        
        return pd.DataFrame(results).sort_values('avg_response_time')
    
    def detect_conversation_topics(self, min_word_length: int = 4, top_n: int = 10) -> Dict:
        """Detect main topics in group conversations using word frequency.
        
        Args:
            min_word_length: Minimum word length to consider
            top_n: Number of top topics to return
            
        Returns:
            Dictionary with topics by time period and user
        """
        # Filter text messages
        text_df = self.df[~self.df['is_media'] & ~self.df['is_system']].copy()
        
        # Stop words
        stop_words = {
            'the', 'is', 'at', 'which', 'on', 'and', 'a', 'to', 'in', 'was',
            'it', 'of', 'for', 'as', 'with', 'be', 'are', 'by', 'this', 'that',
            'from', 'or', 'have', 'an', 'not', 'but', 'what', 'all', 'were',
            'when', 'we', 'there', 'can', 'been', 'has', 'if', 'more', 'her',
            'his', 'they', 'you', 'me', 'my', 'i', 'im', 'dont', 'didnt', 'will',
            'just', 'now', 'like', 'get', 'got', 'going', 'yeah', 'yes', 'okay'
        }
        
        # Overall topics
        all_words = []
        for message in text_df['message']:
            words = re.findall(r'\b[a-zA-Z]+\b', message.lower())
            words = [w for w in words if len(w) >= min_word_length and w not in stop_words]
            all_words.extend(words)
        
        overall_topics = Counter(all_words).most_common(top_n)
        
        # Topics by user
        user_topics = {}
        for author in text_df['author'].unique():
            user_messages = text_df[text_df['author'] == author]['message']
            user_words = []
            for message in user_messages:
                words = re.findall(r'\b[a-zA-Z]+\b', message.lower())
                words = [w for w in words if len(w) >= min_word_length and w not in stop_words]
                user_words.extend(words)
            user_topics[author] = Counter(user_words).most_common(top_n)
        
        # Topics by time period (monthly)
        text_df['month_year'] = text_df['datetime'].dt.to_period('M')
        period_topics = {}
        
        for period in text_df['month_year'].unique():
            period_messages = text_df[text_df['month_year'] == period]['message']
            period_words = []
            for message in period_messages:
                words = re.findall(r'\b[a-zA-Z]+\b', message.lower())
                words = [w for w in words if len(w) >= min_word_length and w not in stop_words]
                period_words.extend(words)
            if period_words:
                period_topics[str(period)] = Counter(period_words).most_common(top_n)
        
        return {
            'overall': overall_topics,
            'by_user': user_topics,
            'by_period': period_topics
        }
    
    def get_user_pair_topics(self, user1: str, user2: str, top_n: int = 10) -> List[Tuple[str, int]]:
        """Find common topics when two specific users are active.
        
        Args:
            user1: First user name
            user2: Second user name
            top_n: Number of top topics
            
        Returns:
            List of (word, count) tuples
        """
        # Get messages from both users
        pair_df = self.df[
            (self.df['author'].isin([user1, user2])) & 
            (~self.df['is_media']) & 
            (~self.df['is_system'])
        ]
        
        stop_words = {
            'the', 'is', 'at', 'which', 'on', 'and', 'a', 'to', 'in', 'was',
            'it', 'of', 'for', 'as', 'with', 'be', 'are', 'by', 'this', 'that',
            'from', 'or', 'have', 'an', 'not', 'but', 'what', 'all', 'were',
            'when', 'we', 'there', 'can', 'been', 'has', 'if', 'more', 'her',
            'his', 'they', 'you', 'me', 'my', 'i', 'im', 'dont', 'didnt'
        }
        
        words = []
        for message in pair_df['message']:
            msg_words = re.findall(r'\b[a-zA-Z]+\b', message.lower())
            msg_words = [w for w in msg_words if len(w) >= 4 and w not in stop_words]
            words.extend(msg_words)
        
        return Counter(words).most_common(top_n)
    
    def get_active_time_overlap(self) -> pd.DataFrame:
        """Find when different users are most active together.
        
        Returns:
            DataFrame with overlap statistics
        """
        # Group by date and hour
        self.df['date_hour'] = self.df['datetime'].dt.floor('H')
        
        # Count messages per user per hour
        hourly_activity = self.df[~self.df['is_system']].groupby(
            ['date_hour', 'author']
        ).size().reset_index(name='message_count')
        
        # Pivot to get users as columns
        activity_pivot = hourly_activity.pivot(
            index='date_hour', 
            columns='author', 
            values='message_count'
        ).fillna(0)
        
        # Calculate overlap (hours where both users were active)
        authors = list(activity_pivot.columns)
        overlaps = []
        
        for i, user1 in enumerate(authors):
            for user2 in authors[i+1:]:
                # Hours where both were active (both > 0 messages)
                overlap_hours = ((activity_pivot[user1] > 0) & (activity_pivot[user2] > 0)).sum()
                
                if overlap_hours > 0:
                    overlaps.append({
                        'user1': user1,
                        'user2': user2,
                        'overlap_hours': overlap_hours,
                        'user1_total_hours': (activity_pivot[user1] > 0).sum(),
                        'user2_total_hours': (activity_pivot[user2] > 0).sum()
                    })
        
        if not overlaps:
            return pd.DataFrame()
        
        overlap_df = pd.DataFrame(overlaps)
        overlap_df['overlap_percentage'] = (
            overlap_df['overlap_hours'] / 
            overlap_df[['user1_total_hours', 'user2_total_hours']].min(axis=1) * 100
        ).round(2)
        
        return overlap_df.sort_values('overlap_hours', ascending=False)
    
    def get_conversation_starters(self) -> pd.DataFrame:
        """Identify who typically starts conversations.
        
        Returns:
            DataFrame with conversation starter statistics
        """
        sorted_df = self.df[~self.df['is_system']].sort_values('datetime').reset_index(drop=True)
        
        # A conversation starts if there's > 1 hour gap from previous message
        conversation_starters = []
        
        for i in range(1, len(sorted_df)):
            time_gap = (sorted_df.iloc[i]['datetime'] - sorted_df.iloc[i-1]['datetime']).total_seconds() / 3600
            
            if time_gap > 1:  # More than 1 hour gap
                conversation_starters.append(sorted_df.iloc[i]['author'])
        
        # Count starters
        starter_counts = Counter(conversation_starters)
        
        results = []
        for author, count in starter_counts.items():
            total_messages = len(self.df[self.df['author'] == author])
            results.append({
                'author': author,
                'conversations_started': count,
                'total_messages': total_messages,
                'starter_percentage': round(count / len(conversation_starters) * 100, 2)
            })
        
        return pd.DataFrame(results).sort_values('conversations_started', ascending=False)
    
    def get_most_active_days_by_pair(self, user1: str, user2: str, top_n: int = 10) -> pd.DataFrame:
        """Find the most active days for a specific user pair.
        
        Args:
            user1: First user
            user2: Second user
            top_n: Number of days to return
            
        Returns:
            DataFrame with most active days for the pair
        """
        pair_df = self.df[
            (self.df['author'].isin([user1, user2])) & 
            (~self.df['is_system'])
        ].copy()
        
        pair_df['date'] = pair_df['datetime'].dt.date
        
        daily_activity = pair_df.groupby(['date', 'author']).size().reset_index(name='message_count')
        
        # Get days with activity from both users
        daily_pivot = daily_activity.pivot(
            index='date', 
            columns='author', 
            values='message_count'
        ).fillna(0)
        
        if user1 in daily_pivot.columns and user2 in daily_pivot.columns:
            daily_pivot['total_pair_messages'] = daily_pivot[user1] + daily_pivot[user2]
            daily_pivot['both_active'] = (daily_pivot[user1] > 0) & (daily_pivot[user2] > 0)
            
            result = daily_pivot[daily_pivot['both_active']].sort_values(
                'total_pair_messages', 
                ascending=False
            ).head(top_n)
            
            return result[[user1, user2, 'total_pair_messages']].reset_index()
        
        return pd.DataFrame()
    
    def get_dominance_score(self) -> pd.DataFrame:
        """Calculate dominance score for each user (how much they dominate conversations).
        
        Returns:
            DataFrame with dominance metrics
        """
        user_stats = []
        total_messages = len(self.df[~self.df['is_system']])
        
        for author in self.df['author'].unique():
            author_messages = self.df[self.df['author'] == author]
            
            # Message count
            msg_count = len(author_messages[~author_messages['is_system']])
            
            # Average message length
            avg_length = author_messages[~author_messages['is_system']]['message_length'].mean()
            
            # Conversation starters
            starters = self.get_conversation_starters()
            starter_count = starters[starters['author'] == author]['conversations_started'].values
            starter_count = starter_count[0] if len(starter_count) > 0 else 0
            
            # Calculate dominance score (weighted)
            message_dominance = (msg_count / total_messages) * 100
            length_factor = min(avg_length / 50, 2)  # Cap at 2x
            starter_factor = (starter_count / max(len(starters), 1)) * 100
            
            dominance_score = (message_dominance * 0.5) + (starter_factor * 0.3) + (length_factor * 10 * 0.2)
            
            user_stats.append({
                'author': author,
                'message_percentage': round(message_dominance, 2),
                'avg_message_length': round(avg_length, 1),
                'conversations_started': starter_count,
                'dominance_score': round(dominance_score, 2)
            })
        
        return pd.DataFrame(user_stats).sort_values('dominance_score', ascending=False)
    
    def get_group_summary(self) -> Dict:
        """Get comprehensive group chat summary.
        
        Returns:
            Dictionary with various group metrics
        """
        total_members = len(self.df['author'].unique())
        total_messages = len(self.df[~self.df['is_system']])
        
        # Most active pair
        pairs = self.get_conversation_pairs(min_interactions=1)
        most_active_pair = pairs[0] if pairs else None
        
        # Conversation starters
        starters = self.get_conversation_starters()
        top_starter = starters.iloc[0]['author'] if not starters.empty else None
        
        # Activity overlap
        overlaps = self.get_active_time_overlap()
        
        return {
            'total_members': total_members,
            'total_messages': total_messages,
            'messages_per_member': round(total_messages / total_members, 2),
            'most_active_pair': most_active_pair,
            'top_conversation_starter': top_starter,
            'total_conversation_pairs': len(pairs),
            'avg_overlap_hours': overlaps['overlap_hours'].mean() if not overlaps.empty else 0
        }
