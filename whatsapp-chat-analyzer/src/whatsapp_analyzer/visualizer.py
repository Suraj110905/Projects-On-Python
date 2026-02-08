"""WhatsApp Chat Visualizer - Create visualizations from chat analysis."""

from typing import Optional, Dict, List
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud
from collections import Counter


class ChatVisualizer:
    """Create visualizations for WhatsApp chat analysis."""
    
    def __init__(self, style: str = 'seaborn-v0_8-darkgrid'):
        """Initialize visualizer with plotting style.
        
        Args:
            style: Matplotlib style to use
        """
        try:
            plt.style.use(style)
        except:
            plt.style.use('default')
        
        sns.set_palette("husl")
        self.colors = sns.color_palette("husl", 10)
        
    def _get_colors(self, n: int):
        """Get n colors for plotting.
        
        Args:
            n: Number of colors needed
            
        Returns:
            List of colors
        """
        if n <= len(self.colors):
            return self.colors[:n]
        else:
            # Generate more colors if needed
            return sns.color_palette("husl", n)
    
    def plot_user_message_distribution(
        self, 
        user_stats: pd.DataFrame,
        save_path: Optional[str] = None
    ) -> plt.Figure:
        """Plot message distribution by user.
        
        Args:
            user_stats: DataFrame from ChatAnalyzer.get_user_stats()
            save_path: Optional path to save the figure
            
        Returns:
            Matplotlib figure
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Get appropriate number of colors
        colors = self._get_colors(len(user_stats))
        
        # Bar chart
        ax1.bar(user_stats['author'], user_stats['total_messages'], color=colors)
        ax1.set_xlabel('User', fontsize=12)
        ax1.set_ylabel('Number of Messages', fontsize=12)
        ax1.set_title('Messages per User', fontsize=14, fontweight='bold')
        ax1.tick_params(axis='x', rotation=45)
        
        # Pie chart
        ax2.pie(
            user_stats['total_messages'], 
            labels=user_stats['author'],
            autopct='%1.1f%%',
            colors=colors,
            startangle=90
        )
        ax2.set_title('Message Distribution', fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            
        return fig
    
    def plot_activity_timeline(
        self,
        timeline_df: pd.DataFrame,
        save_path: Optional[str] = None,
        interactive: bool = True
    ):
        """Plot message activity over time.
        
        Args:
            timeline_df: DataFrame from ChatAnalyzer.get_activity_timeline()
            save_path: Optional path to save the figure
            interactive: Use plotly for interactive chart
            
        Returns:
            Plotly figure if interactive, else Matplotlib figure
        """
        if interactive:
            fig = px.line(
                timeline_df,
                x='datetime',
                y='message_count',
                color='author',
                title='Message Activity Over Time',
                labels={'datetime': 'Date', 'message_count': 'Number of Messages'}
            )
            fig.update_layout(
                hovermode='x unified',
                xaxis_title='Date',
                yaxis_title='Number of Messages'
            )
            
            if save_path:
                fig.write_html(save_path)
                
            return fig
        else:
            fig, ax = plt.subplots(figsize=(15, 6))
            
            for author in timeline_df['author'].unique():
                author_data = timeline_df[timeline_df['author'] == author]
                ax.plot(author_data['datetime'], author_data['message_count'], label=author, marker='o')
            
            ax.set_xlabel('Date', fontsize=12)
            ax.set_ylabel('Number of Messages', fontsize=12)
            ax.set_title('Message Activity Over Time', fontsize=14, fontweight='bold')
            ax.legend()
            ax.grid(True, alpha=0.3)
            plt.xticks(rotation=45)
            plt.tight_layout()
            
            if save_path:
                plt.savefig(save_path, dpi=300, bbox_inches='tight')
                
            return fig
    
    def plot_hourly_activity(
        self,
        hourly_df: pd.DataFrame,
        save_path: Optional[str] = None
    ) -> plt.Figure:
        """Plot hourly activity heatmap.
        
        Args:
            hourly_df: DataFrame from ChatAnalyzer.get_hourly_activity()
            save_path: Optional path to save the figure
            
        Returns:
            Matplotlib figure
        """
        # Pivot for heatmap
        pivot_data = hourly_df.pivot(index='author', columns='hour', values='message_count')
        pivot_data = pivot_data.fillna(0)
        
        fig, ax = plt.subplots(figsize=(14, 6))
        sns.heatmap(
            pivot_data,
            annot=True,
            fmt='g',
            cmap='YlOrRd',
            ax=ax,
            cbar_kws={'label': 'Message Count'}
        )
        ax.set_title('Message Activity by Hour', fontsize=14, fontweight='bold')
        ax.set_xlabel('Hour of Day', fontsize=12)
        ax.set_ylabel('User', fontsize=12)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            
        return fig
    
    def plot_daily_activity(
        self,
        daily_df: pd.DataFrame,
        save_path: Optional[str] = None
    ) -> plt.Figure:
        """Plot daily activity by day of week.
        
        Args:
            daily_df: DataFrame from ChatAnalyzer.get_daily_activity()
            save_path: Optional path to save the figure
            
        Returns:
            Matplotlib figure
        """
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Get colors for all authors
        authors = daily_df['author'].unique()
        colors = self._get_colors(len(authors))
        
        # Group data by author
        for i, author in enumerate(authors):
            author_data = daily_df[daily_df['author'] == author]
            ax.plot(
                author_data['day_of_week'],
                author_data['message_count'],
                marker='o',
                label=author,
                linewidth=2,
                markersize=8,
                color=colors[i]
            )
        
        ax.set_xlabel('Day of Week', fontsize=12)
        ax.set_ylabel('Number of Messages', fontsize=12)
        ax.set_title('Message Activity by Day of Week', fontsize=14, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            
        return fig
    
    def create_wordcloud(
        self,
        word_freq: Dict,
        save_path: Optional[str] = None,
        max_words: int = 100
    ) -> plt.Figure:
        """Create a word cloud from word frequency data.
        
        Args:
            word_freq: Dictionary with word frequency data from ChatAnalyzer
            save_path: Optional path to save the figure
            max_words: Maximum number of words to include
            
        Returns:
            Matplotlib figure
        """
        # Convert most_common list to dict
        word_dict = dict(word_freq['most_common'][:max_words])
        
        wordcloud = WordCloud(
            width=1600,
            height=800,
            background_color='white',
            colormap='viridis',
            max_words=max_words,
            relative_scaling=0.5,
            min_font_size=10
        ).generate_from_frequencies(word_dict)
        
        fig, ax = plt.subplots(figsize=(16, 8))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')
        ax.set_title('Most Common Words', fontsize=16, fontweight='bold', pad=20)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            
        return fig
    
    def plot_emoji_distribution(
        self,
        emoji_data: Dict,
        top_n: int = 15,
        save_path: Optional[str] = None
    ) -> plt.Figure:
        """Plot emoji usage distribution.
        
        Args:
            emoji_data: Dictionary from ChatAnalyzer.analyze_emojis()
            top_n: Number of top emojis to display
            save_path: Optional path to save the figure
            
        Returns:
            Matplotlib figure
        """
        emojis, counts = zip(*emoji_data['most_common'][:top_n])
        
        # Get appropriate colors
        colors = self._get_colors(len(emojis))
        
        fig, ax = plt.subplots(figsize=(12, 6))
        bars = ax.barh(range(len(emojis)), counts, color=colors)
        
        ax.set_yticks(range(len(emojis)))
        ax.set_yticklabels(emojis, fontsize=14)
        ax.set_xlabel('Count', fontsize=12)
        ax.set_title(f'Top {top_n} Most Used Emojis', fontsize=14, fontweight='bold')
        ax.invert_yaxis()
        
        # Add count labels
        for i, (bar, count) in enumerate(zip(bars, counts)):
            ax.text(count, i, f' {count}', va='center', fontsize=10)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            
        return fig
    
    def plot_sentiment_distribution(
        self,
        sentiment_summary: Dict,
        save_path: Optional[str] = None
    ) -> plt.Figure:
        """Plot sentiment distribution.
        
        Args:
            sentiment_summary: Dictionary from ChatAnalyzer.get_sentiment_summary()
            save_path: Optional path to save the figure
            
        Returns:
            Matplotlib figure
        """
        overall = sentiment_summary['overall']
        sentiments = ['Positive', 'Neutral', 'Negative']
        counts = [overall['positive'], overall['neutral'], overall['negative']]
        colors_sentiment = ['#2ecc71', '#95a5a6', '#e74c3c']
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Overall sentiment pie chart
        ax1.pie(counts, labels=sentiments, autopct='%1.1f%%', colors=colors_sentiment, startangle=90)
        ax1.set_title('Overall Sentiment Distribution', fontsize=14, fontweight='bold')
        
        # Per-user sentiment comparison
        if 'per_user' in sentiment_summary:
            users = list(sentiment_summary['per_user'].keys())
            pos_counts = [sentiment_summary['per_user'][u]['positive'] for u in users]
            neu_counts = [sentiment_summary['per_user'][u]['neutral'] for u in users]
            neg_counts = [sentiment_summary['per_user'][u]['negative'] for u in users]
            
            x = range(len(users))
            width = 0.25
            
            ax2.bar([i - width for i in x], pos_counts, width, label='Positive', color=colors_sentiment[0])
            ax2.bar(x, neu_counts, width, label='Neutral', color=colors_sentiment[1])
            ax2.bar([i + width for i in x], neg_counts, width, label='Negative', color=colors_sentiment[2])
            
            ax2.set_xlabel('User', fontsize=12)
            ax2.set_ylabel('Message Count', fontsize=12)
            ax2.set_title('Sentiment by User', fontsize=14, fontweight='bold')
            ax2.set_xticks(x)
            ax2.set_xticklabels(users, rotation=45, ha='right')
            ax2.legend()
            ax2.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            
        return fig
    
    def plot_response_times(
        self,
        response_stats: Dict,
        save_path: Optional[str] = None
    ) -> plt.Figure:
        """Plot response time statistics.
        
        Args:
            response_stats: Dictionary from ChatAnalyzer.get_response_time_stats()
            save_path: Optional path to save the figure
            
        Returns:
            Matplotlib figure
        """
        if not response_stats or 'per_user' not in response_stats:
            print("No response time data available")
            return None
            
        users = list(response_stats['per_user'].keys())
        mean_times = [response_stats['per_user'][u]['mean'] for u in users]
        median_times = [response_stats['per_user'][u]['median'] for u in users]
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        x = range(len(users))
        width = 0.35
        
        ax.bar([i - width/2 for i in x], mean_times, width, label='Mean', color=self.colors[0])
        ax.bar([i + width/2 for i in x], median_times, width, label='Median', color=self.colors[1])
        
        ax.set_xlabel('User', fontsize=12)
        ax.set_ylabel('Response Time (minutes)', fontsize=12)
        ax.set_title('Average Response Times by User', fontsize=14, fontweight='bold')
        ax.set_xticks(x)
        ax.set_xticklabels(users, rotation=45, ha='right')
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            
        return fig
    
    def create_interactive_dashboard(
        self,
        user_stats: pd.DataFrame,
        hourly_df: pd.DataFrame,
        emoji_data: Dict
    ):
        """Create an interactive dashboard with multiple visualizations.
        
        Args:
            user_stats: DataFrame from ChatAnalyzer.get_user_stats()
            hourly_df: DataFrame from ChatAnalyzer.get_hourly_activity()
            emoji_data: Dictionary from ChatAnalyzer.analyze_emojis()
            
        Returns:
            Plotly figure with subplots
        """
        from plotly.subplots import make_subplots
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Messages per User', 'Hourly Activity', 
                          'Top Emojis', 'Message Statistics'),
            specs=[[{"type": "bar"}, {"type": "scatter"}],
                   [{"type": "bar"}, {"type": "table"}]]
        )
        
        # Messages per user
        fig.add_trace(
            go.Bar(x=user_stats['author'], y=user_stats['total_messages'], name='Messages'),
            row=1, col=1
        )
        
        # Hourly activity
        for author in hourly_df['author'].unique():
            author_data = hourly_df[hourly_df['author'] == author]
            fig.add_trace(
                go.Scatter(x=author_data['hour'], y=author_data['message_count'],
                          mode='lines+markers', name=author),
                row=1, col=2
            )
        
        # Top emojis
        emojis, counts = zip(*emoji_data['most_common'][:10])
        fig.add_trace(
            go.Bar(x=list(counts), y=list(emojis), orientation='h', name='Emoji Count'),
            row=2, col=1
        )
        
        # Statistics table
        fig.add_trace(
            go.Table(
                header=dict(values=['User', 'Messages', 'Avg Length', 'Media']),
                cells=dict(values=[
                    user_stats['author'],
                    user_stats['total_messages'],
                    user_stats['avg_message_length'].round(1),
                    user_stats['media_messages']
                ])
            ),
            row=2, col=2
        )
        
        fig.update_layout(height=800, showlegend=True, title_text="WhatsApp Chat Analysis Dashboard")
        
        return fig
