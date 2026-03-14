"""WhatsApp Chat Visualizer - Create visualizations from chat analysis."""

from typing import Optional, Dict
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from wordcloud import WordCloud


class ChatVisualizer:

    def __init__(self, style='seaborn-v0_8-darkgrid'):
        try:
            plt.style.use(style)
        except:
            plt.style.use('default')

        sns.set_palette("husl")
        self.colors = sns.color_palette("husl", 10)

    def _get_colors(self, n):
        if n <= len(self.colors):
            return self.colors[:n]
        return sns.color_palette("husl", n)

    # ---------------------------------------------------
    # USER MESSAGE DISTRIBUTION
    # ---------------------------------------------------

    def plot_user_message_distribution(self, user_stats, save_path=None):

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

        colors = self._get_colors(len(user_stats))

        ax1.bar(user_stats['author'], user_stats['total_messages'], color=colors)
        ax1.set_title("Messages per User")
        ax1.set_xlabel("User")
        ax1.set_ylabel("Messages")
        ax1.tick_params(axis='x', rotation=45)

        ax2.pie(
            user_stats['total_messages'],
            labels=user_stats['author'],
            autopct='%1.1f%%',
            colors=colors,
            startangle=90
        )

        ax2.set_title("Message Distribution")

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path)

        return fig

    # ---------------------------------------------------
    # ACTIVITY TIMELINE
    # ---------------------------------------------------

    def plot_activity_timeline(self, timeline_df, interactive=True):

        if interactive:

            fig = px.line(
                timeline_df,
                x='datetime',
                y='message_count',
                color='author',
                title="Message Activity Over Time"
            )

            return fig

        else:

            fig, ax = plt.subplots(figsize=(15,6))

            for author in timeline_df['author'].unique():
                data = timeline_df[timeline_df['author'] == author]

                ax.plot(
                    data['datetime'],
                    data['message_count'],
                    label=author
                )

            ax.set_xlabel("Date")
            ax.set_ylabel("Messages")
            ax.set_title("Message Activity")
            ax.legend()

            plt.xticks(rotation=45)
            plt.tight_layout()

            return fig

    # ---------------------------------------------------
    # HOURLY ACTIVITY
    # ---------------------------------------------------

    def plot_hourly_activity(self, hourly_df):

        pivot_data = hourly_df.pivot(
            index='author',
            columns='hour',
            values='message_count'
        ).fillna(0)

        fig, ax = plt.subplots(figsize=(14,6))

        sns.heatmap(
            pivot_data,
            annot=True,
            fmt='g',
            cmap='YlOrRd',
            ax=ax
        )

        ax.set_title("Message Activity by Hour")
        ax.set_xlabel("Hour")
        ax.set_ylabel("User")

        plt.tight_layout()

        return fig

    # ---------------------------------------------------
    # DAILY ACTIVITY
    # ---------------------------------------------------

    def plot_daily_activity(self, daily_df):

        fig, ax = plt.subplots(figsize=(12,6))

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

        ax.set_xlabel("Day")
        ax.set_ylabel("Messages")
        ax.set_title("Daily Activity")
        ax.legend()

        plt.xticks(rotation=45)
        plt.tight_layout()

        return fig

    # ---------------------------------------------------
    # WORD CLOUD
    # ---------------------------------------------------

    def create_wordcloud(self, word_freq, max_words=100):

        if not word_freq or len(word_freq['most_common']) == 0:
            return None

        word_dict = dict(word_freq['most_common'][:max_words])

        wordcloud = WordCloud(
            width=1600,
            height=800,
            background_color='white',
            colormap='viridis'
        ).generate_from_frequencies(word_dict)

        fig, ax = plt.subplots(figsize=(16,8))

        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis("off")
        ax.set_title("Most Common Words")

        return fig

    # ---------------------------------------------------
    # EMOJI DISTRIBUTION
    # ---------------------------------------------------

    def plot_emoji_distribution(self, emoji_data, top_n=15):

        if not emoji_data or len(emoji_data['most_common']) == 0:
            return None

        emojis, counts = zip(*emoji_data['most_common'][:top_n])

        fig, ax = plt.subplots(figsize=(12,6))

        ax.barh(range(len(emojis)), counts)

        ax.set_yticks(range(len(emojis)))
        ax.set_yticklabels(emojis, fontsize=14)
        ax.set_xlabel("Count")
        ax.set_title("Top Emojis")

        ax.invert_yaxis()

        plt.tight_layout()

        return fig

    # ---------------------------------------------------
    # SENTIMENT DISTRIBUTION
    # ---------------------------------------------------

    def plot_sentiment_distribution(self, sentiment_summary):

        overall = sentiment_summary['overall']

        sentiments = ["Positive", "Neutral", "Negative"]

        counts = [
            overall['positive'],
            overall['neutral'],
            overall['negative']
        ]

        colors = ['#2ecc71', '#95a5a6', '#e74c3c']

        fig, ax = plt.subplots(figsize=(8,6))

        ax.pie(
            counts,
            labels=sentiments,
            autopct='%1.1f%%',
            colors=colors,
            startangle=90
        )

        ax.set_title("Sentiment Distribution")

        return fig

    # ---------------------------------------------------
    # RESPONSE TIME
    # ---------------------------------------------------

    def plot_response_times(self, response_stats):

        if not response_stats or 'per_user' not in response_stats:
            return None

        users = []
        means = []

        for user, stats in response_stats['per_user'].items():
            users.append(user)
            means.append(stats['mean'])

        fig, ax = plt.subplots(figsize=(10,6))

        ax.bar(users, means)

        ax.set_xlabel("User")
        ax.set_ylabel("Average Response Time (minutes)")
        ax.set_title("Average Response Time by User")

        plt.xticks(rotation=45)
        plt.tight_layout()

        return fig
