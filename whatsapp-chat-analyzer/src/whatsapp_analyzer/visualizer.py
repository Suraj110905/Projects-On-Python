"""WhatsApp Chat Visualizer - Create visualizations from chat analysis."""

from typing import Optional, Dict
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud


class ChatVisualizer:
    """Create visualizations for WhatsApp chat analysis."""

    def __init__(self, style: str = 'seaborn-v0_8-darkgrid'):
        try:
            plt.style.use(style)
        except:
            plt.style.use('default')

        sns.set_palette("husl")
        self.colors = sns.color_palette("husl", 10)

    def _get_colors(self, n: int):
        if n <= len(self.colors):
            return self.colors[:n]
        else:
            return sns.color_palette("husl", n)
    # ---------------------------------------------------
# RESPONSE TIME VISUALIZATION
# ---------------------------------------------------

def plot_response_times(
    self,
    response_stats: dict,
    save_path: Optional[str] = None
) -> plt.Figure:

    if not response_stats or 'per_user' not in response_stats:
        return None

    users = []
    means = []

    for user, stats in response_stats['per_user'].items():
        users.append(user)
        means.append(stats['mean'])

    if len(users) == 0:
        return None

    fig, ax = plt.subplots(figsize=(10,6))

    ax.bar(users, means)

    ax.set_xlabel("User")
    ax.set_ylabel("Average Response Time (minutes)")
    ax.set_title("Average Response Time by User")

    plt.xticks(rotation=45)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path)

    return fig

    # ---------------------------------------------------
    # USER MESSAGE DISTRIBUTION
    # ---------------------------------------------------

    def plot_user_message_distribution(
        self,
        user_stats: pd.DataFrame,
        save_path: Optional[str] = None
    ) -> plt.Figure:

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        colors = self._get_colors(len(user_stats))

        ax1.bar(user_stats['author'], user_stats['total_messages'], color=colors)
        ax1.set_xlabel('User')
        ax1.set_ylabel('Messages')
        ax1.set_title('Messages per User')
        ax1.tick_params(axis='x', rotation=45)

        ax2.pie(
            user_stats['total_messages'],
            labels=user_stats['author'],
            autopct='%1.1f%%',
            colors=colors,
            startangle=90
        )

        ax2.set_title('Message Distribution')

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300)

        return fig

    # ---------------------------------------------------
    # ACTIVITY TIMELINE
    # ---------------------------------------------------

    def plot_activity_timeline(
        self,
        timeline_df: pd.DataFrame,
        save_path: Optional[str] = None,
        interactive: bool = True
    ):

        if interactive:

            fig = px.line(
                timeline_df,
                x='datetime',
                y='message_count',
                color='author',
                title='Message Activity Over Time'
            )

            if save_path:
                fig.write_html(save_path)

            return fig

        else:

            fig, ax = plt.subplots(figsize=(15, 6))

            for author in timeline_df['author'].unique():
                data = timeline_df[timeline_df['author'] == author]

                ax.plot(data['datetime'], data['message_count'], label=author)

            ax.set_xlabel('Date')
            ax.set_ylabel('Messages')
            ax.set_title('Message Activity')
            ax.legend()

            plt.xticks(rotation=45)
            plt.tight_layout()

            return fig

    # ---------------------------------------------------
    # HOURLY ACTIVITY
    # ---------------------------------------------------

    def plot_hourly_activity(
        self,
        hourly_df: pd.DataFrame,
        save_path: Optional[str] = None
    ) -> plt.Figure:

        pivot_data = hourly_df.pivot(
            index='author',
            columns='hour',
            values='message_count'
        ).fillna(0)

        fig, ax = plt.subplots(figsize=(14, 6))

        sns.heatmap(
            pivot_data,
            annot=True,
            fmt='g',
            cmap='YlOrRd',
            ax=ax
        )

        ax.set_title('Message Activity by Hour')
        ax.set_xlabel('Hour')
        ax.set_ylabel('User')

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path)

        return fig

    # ---------------------------------------------------
    # DAILY ACTIVITY
    # ---------------------------------------------------

    def plot_daily_activity(
        self,
        daily_df: pd.DataFrame,
        save_path: Optional[str] = None
    ) -> plt.Figure:

        fig, ax = plt.subplots(figsize=(12, 6))

        authors = daily_df['author'].unique()
        colors = self._get_colors(len(authors))

        for i, author in enumerate(authors):

            data = daily_df[daily_df['author'] == author]

            ax.plot(
                data['day_of_week'],
                data['message_count'],
                marker='o',
                label=author,
                color=colors[i]
            )

        ax.set_xlabel('Day')
        ax.set_ylabel('Messages')
        ax.set_title('Daily Activity')
        ax.legend()

        plt.xticks(rotation=45)
        plt.tight_layout()

        return fig

    # ---------------------------------------------------
    # WORD CLOUD
    # ---------------------------------------------------

    def create_wordcloud(
        self,
        word_freq: Dict,
        save_path: Optional[str] = None,
        max_words: int = 100
    ) -> plt.Figure:

        if not word_freq or len(word_freq['most_common']) == 0:
            print("No words available")
            return None

        word_dict = dict(word_freq['most_common'][:max_words])

        wordcloud = WordCloud(
            width=1600,
            height=800,
            background_color='white',
            colormap='viridis'
        ).generate_from_frequencies(word_dict)

        fig, ax = plt.subplots(figsize=(16, 8))

        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')
        ax.set_title('Most Common Words')

        return fig

    # ---------------------------------------------------
    # EMOJI DISTRIBUTION (FIXED)
    # ---------------------------------------------------

    def plot_emoji_distribution(
        self,
        emoji_data: Dict,
        top_n: int = 15,
        save_path: Optional[str] = None
    ) -> plt.Figure:

        if not emoji_data or 'most_common' not in emoji_data or len(emoji_data['most_common']) == 0:
            print("No emojis found")
            return None

        emojis, counts = zip(*emoji_data['most_common'][:top_n])

        fig, ax = plt.subplots(figsize=(12, 6))

        ax.barh(range(len(emojis)), counts, color=self._get_colors(len(emojis)))

        ax.set_yticks(range(len(emojis)))
        ax.set_yticklabels(emojis, fontsize=14)
        ax.set_xlabel('Count')
        ax.set_title('Top Emojis')

        ax.invert_yaxis()

        plt.tight_layout()

        return fig

    # ---------------------------------------------------
    # SENTIMENT DISTRIBUTION (FIXED)
    # ---------------------------------------------------

    def plot_sentiment_distribution(
        self,
        sentiment_summary: Dict,
        save_path: Optional[str] = None
    ) -> plt.Figure:

        if not sentiment_summary or 'overall' not in sentiment_summary:
            print("No sentiment data available")
            return None

        overall = sentiment_summary['overall']

        sentiments = ['Positive', 'Neutral', 'Negative']

        counts = [
            overall.get('positive', 0),
            overall.get('neutral', 0),
            overall.get('negative', 0)
        ]

        colors = ['#2ecc71', '#95a5a6', '#e74c3c']

        fig, ax = plt.subplots(figsize=(8, 6))

        ax.pie(
            counts,
            labels=sentiments,
            autopct='%1.1f%%',
            colors=colors,
            startangle=90
        )

        ax.set_title('Sentiment Distribution')

        return fig
