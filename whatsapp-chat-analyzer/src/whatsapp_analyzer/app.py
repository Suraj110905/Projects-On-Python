"""Streamlit Dashboard for WhatsApp Chat Analysis."""

import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from whatsapp_analyzer.parser import ChatParser
from whatsapp_analyzer.analyzer import ChatAnalyzer
from whatsapp_analyzer.visualizer import ChatVisualizer
from whatsapp_analyzer.group_analyzer import GroupChatAnalyzer


# Page configuration
st.set_page_config(
    page_title="WhatsApp Chat Analyzer",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        color: #25D366;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    </style>
""", unsafe_allow_html=True)


def main():
    """Main application function."""
    
    st.markdown('<h1 class="main-header">💬 WhatsApp Chat Analyzer</h1>', unsafe_allow_html=True)
    st.markdown("### Analyze your WhatsApp chats with advanced insights and visualizations")
    
    # Sidebar
    with st.sidebar:
        st.header("📁 Upload Chat")
        st.markdown("""
        **How to export your WhatsApp chat:**
        1. Open WhatsApp chat
        2. Tap ⋮ (menu) → More → Export chat
        3. Choose 'Without Media'
        4. Upload the .txt file here
        """)
        
        uploaded_file = st.file_uploader(
            "Choose a WhatsApp chat export file",
            type=['txt'],
            help="Upload your WhatsApp chat export (.txt file)"
        )
        
        st.markdown("---")
        st.markdown("### 🎯 Features")
        st.markdown("""
        - 📊 User Statistics
        - 📈 Activity Timeline
        - ⏰ Time-based Analysis
        - 😀 Emoji Analysis
        - 💬 Word Frequency
        - 🎭 Sentiment Analysis
        - ⚡ Response Times
        """)
    
    if uploaded_file is not None:
        try:
            # Save uploaded file temporarily
            temp_path = f"temp_{uploaded_file.name}"
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Parse chat
            with st.spinner("Parsing chat data..."):
                parser = ChatParser(temp_path)
                df = parser.load_chat()
                chat_info = parser.get_chat_info()
            
            # Analyze chat
            with st.spinner("Analyzing chat data..."):
                analyzer = ChatAnalyzer(df)
                visualizer = ChatVisualizer()
            
            # Display chat info
            st.success(f"✅ Successfully loaded chat with {chat_info['total_messages']} messages!")
            
            # Overview metrics
            st.header("📊 Chat Overview")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Messages", f"{chat_info['total_messages']:,}")
            with col2:
                st.metric("Participants", chat_info['participants'])
            with col3:
                st.metric("Text Messages", f"{chat_info['text_messages']:,}")
            with col4:
                st.metric("Media Shared", f"{chat_info['media_messages']:,}")
            
            col5, col6 = st.columns(2)
            with col5:
                st.metric("Start Date", chat_info['date_range']['start'].strftime('%Y-%m-%d'))
            with col6:
                st.metric("End Date", chat_info['date_range']['end'].strftime('%Y-%m-%d'))
            
            # Check if group chat
            is_group_chat = chat_info['participants'] > 2
            
            # Tabs for different analyses
            if is_group_chat:
                tabs = st.tabs([
                    "👥 User Stats",
                    "📈 Activity",
                    "😀 Emojis",
                    "💬 Words",
                    "🎭 Sentiment",
                    "⚡ Response Times",
                    "👫 Group Analysis"
                ])
                tab1, tab2, tab3, tab4, tab5, tab6, tab7 = tabs
            else:
                tabs = st.tabs([
                    "👥 User Stats",
                    "📈 Activity",
                    "😀 Emojis",
                    "💬 Words",
                    "🎭 Sentiment",
                    "⚡ Response Times"
                ])
                tab1, tab2, tab3, tab4, tab5, tab6 = tabs
            
            # Tab 1: User Statistics
            with tab1:
                st.header("👥 User Statistics")
                user_stats = analyzer.get_user_stats()
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("📊 Message Distribution")
                    fig = visualizer.plot_user_message_distribution(user_stats)
                    st.pyplot(fig)
                
                with col2:
                    st.subheader("📋 Detailed Statistics")
                    st.dataframe(
                        user_stats.style.format({
                            'avg_message_length': '{:.1f}',
                            'avg_words_per_message': '{:.1f}',
                            'message_percentage': '{:.1f}%'
                        }),
                        use_container_width=True
                    )
            
            # Tab 2: Activity Analysis
            with tab2:
                st.header("📈 Activity Analysis")
                
                # Timeline
                st.subheader("📅 Activity Timeline")
                freq = st.selectbox("Select frequency:", ["Daily", "Weekly", "Monthly"])
                freq_map = {"Daily": "D", "Weekly": "W", "Monthly": "M"}
                timeline = analyzer.get_activity_timeline(freq=freq_map[freq])
                fig_timeline = visualizer.plot_activity_timeline(timeline, interactive=True)
                st.plotly_chart(fig_timeline, use_container_width=True)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("⏰ Hourly Activity")
                    hourly = analyzer.get_hourly_activity()
                    fig_hourly = visualizer.plot_hourly_activity(hourly)
                    st.pyplot(fig_hourly)
                
                with col2:
                    st.subheader("📆 Daily Activity")
                    daily = analyzer.get_daily_activity()
                    fig_daily = visualizer.plot_daily_activity(daily)
                    st.pyplot(fig_daily)
                
                # Most active days
                st.subheader("🔥 Most Active Days")
                active_days = analyzer.get_most_active_days(top_n=10)
                st.dataframe(active_days, use_container_width=True)
            
            # Tab 3: Emoji Analysis
            with tab3:
                st.header("😀 Emoji Analysis")
                emoji_data = analyzer.analyze_emojis(top_n=20)
                
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    st.metric("Total Emojis Used", f"{emoji_data['total_emojis']:,}")
                    st.metric("Unique Emojis", emoji_data['unique_emojis'])
                    
                    st.subheader("Top 10 Emojis")
                    for emoji_char, count in emoji_data['most_common'][:10]:
                        st.markdown(f"**{emoji_char}** - {count} times")
                
                with col2:
                    st.subheader("📊 Emoji Distribution")
                    fig_emoji = visualizer.plot_emoji_distribution(emoji_data, top_n=15)
                    st.pyplot(fig_emoji)
                
                # Per-user emojis
                st.subheader("👤 Emoji Usage by User")
                for user, user_emojis in emoji_data['per_user'].items():
                    if user_emojis:
                        with st.expander(f"**{user}**"):
                            emoji_df = pd.DataFrame(user_emojis, columns=['Emoji', 'Count'])
                            st.dataframe(emoji_df, use_container_width=True)
            
            # Tab 4: Word Analysis
            with tab4:
                st.header("💬 Word Frequency Analysis")
                
                min_length = st.slider("Minimum word length:", 3, 10, 3)
                word_data = analyzer.analyze_word_frequency(top_n=30, min_length=min_length)
                
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    st.metric("Total Words", f"{word_data['total_words']:,}")
                    st.metric("Unique Words", f"{word_data['unique_words']:,}")
                    
                    st.subheader("Top 15 Words")
                    for word, count in word_data['most_common'][:15]:
                        st.markdown(f"**{word}** - {count}")
                
                with col2:
                    st.subheader("☁️ Word Cloud")
                    fig_wordcloud = visualizer.create_wordcloud(word_data, max_words=100)
                    st.pyplot(fig_wordcloud)
                
                # Per-user words
                st.subheader("👤 Most Used Words by User")
                for user, user_words in word_data['per_user'].items():
                    if user_words:
                        with st.expander(f"**{user}**"):
                            words_df = pd.DataFrame(user_words[:20], columns=['Word', 'Count'])
                            st.dataframe(words_df, use_container_width=True)
            
            # Tab 5: Sentiment Analysis
            with tab5:
                st.header("🎭 Sentiment Analysis")
                sentiment_summary = analyzer.get_sentiment_summary()
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("Overall Sentiment")
                    overall = sentiment_summary['overall']
                    st.metric("Positive Messages", overall['positive'], 
                             delta=f"{(overall['positive']/sum([overall['positive'], overall['neutral'], overall['negative']]) * 100):.1f}%")
                    st.metric("Neutral Messages", overall['neutral'],
                             delta=f"{(overall['neutral']/sum([overall['positive'], overall['neutral'], overall['negative']]) * 100):.1f}%")
                    st.metric("Negative Messages", overall['negative'],
                             delta=f"{(overall['negative']/sum([overall['positive'], overall['neutral'], overall['negative']]) * 100):.1f}%")
                
                with col2:
                    st.subheader("📊 Sentiment Distribution")
                    fig_sentiment = visualizer.plot_sentiment_distribution(sentiment_summary)
                    st.pyplot(fig_sentiment)
                
                # Per-user sentiment
                st.subheader("👤 Sentiment by User")
                for user, user_sentiment in sentiment_summary['per_user'].items():
                    with st.expander(f"**{user}**"):
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric("Positive", user_sentiment['positive'])
                        with col2:
                            st.metric("Neutral", user_sentiment['neutral'])
                        with col3:
                            st.metric("Negative", user_sentiment['negative'])
                        with col4:
                            st.metric("Avg Score", f"{user_sentiment['avg_compound']:.3f}")
            
            # Tab 6: Response Times
            with tab6:
                st.header("⚡ Response Time Analysis")
                response_stats = analyzer.get_response_time_stats()
                
                if response_stats:
                    col1, col2 = st.columns([1, 2])
                    
                    with col1:
                        st.subheader("Overall Statistics")
                        overall = response_stats['overall']
                        st.metric("Mean Response Time", f"{overall['mean']:.1f} min")
                        st.metric("Median Response Time", f"{overall['median']:.1f} min")
                        st.metric("Std Deviation", f"{overall['std']:.1f} min")
                        
                        st.subheader("👤 By User")
                        for user, stats in response_stats['per_user'].items():
                            with st.expander(f"**{user}**"):
                                st.write(f"Mean: {stats['mean']:.1f} minutes")
                                st.write(f"Median: {stats['median']:.1f} minutes")
                                st.write(f"Total Responses: {stats['total_responses']}")
                    
                    with col2:
                        st.subheader("📊 Response Times Comparison")
                        fig_response = visualizer.plot_response_times(response_stats)
                        if fig_response:
                            st.pyplot(fig_response)
                else:
                    st.info("Not enough data to calculate response times.")
            
            # Tab 7: Group Analysis (only for group chats)
            if is_group_chat:
                with tab7:
                    st.header("👫 Group Chat Analysis")
                    st.markdown("*Advanced analysis for group conversations with 3+ participants*")
                    
                    # Initialize group analyzer
                    group_analyzer = GroupChatAnalyzer(df)
                    
                    # Group summary
                    st.subheader("📊 Group Summary")
                    summary = group_analyzer.get_group_summary()
                    
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Total Members", summary['total_members'])
                    with col2:
                        st.metric("Messages/Member", f"{summary['messages_per_member']:.0f}")
                    with col3:
                        st.metric("Conversation Pairs", summary['total_conversation_pairs'])
                    with col4:
                        st.metric("Avg Overlap Hours", f"{summary['avg_overlap_hours']:.0f}")
                    
                    if summary['most_active_pair']:
                        st.info(f"🔥 Most Active Pair: **{summary['most_active_pair'][0]}** ↔️ **{summary['most_active_pair'][1]}** ({summary['most_active_pair'][2]} interactions)")
                    
                    if summary['top_conversation_starter']:
                        st.info(f"🚀 Top Conversation Starter: **{summary['top_conversation_starter']}**")
                    
                    st.markdown("---")
                    
                    # Dominance Score
                    st.subheader("🏆 Dominance Score")
                    st.markdown("*Who dominates the conversation based on message count, length, and conversation starters*")
                    dominance = group_analyzer.get_dominance_score()
                    st.dataframe(dominance, use_container_width=True)
                    
                    st.markdown("---")
                    
                    # Interaction Matrix
                    st.subheader("🔗 Interaction Matrix")
                    st.markdown("*Who responds to whom? (rows respond to columns)*")
                    interaction_matrix = group_analyzer.get_interaction_matrix()
                    st.dataframe(interaction_matrix.style.background_gradient(cmap='YlOrRd'), use_container_width=True)
                    
                    st.markdown("---")
                    
                    # Conversation Pairs
                    st.subheader("👥 Most Active Conversation Pairs")
                    pairs = group_analyzer.get_conversation_pairs(min_interactions=5)
                    
                    if pairs:
                        pairs_df = pd.DataFrame(pairs, columns=['User 1', 'User 2', 'Interactions'])
                        st.dataframe(pairs_df.head(10), use_container_width=True)
                        
                        # Select pair for detailed analysis
                        st.markdown("---")
                        st.subheader("🔍 Pair-Specific Analysis")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            user1 = st.selectbox("Select User 1:", chat_info['participant_names'])
                        with col2:
                            other_users = [u for u in chat_info['participant_names'] if u != user1]
                            user2 = st.selectbox("Select User 2:", other_users)
                        
                        if user1 and user2:
                            # Topics for this pair
                            st.markdown(f"**Common Topics: {user1} ↔️ {user2}**")
                            pair_topics = group_analyzer.get_user_pair_topics(user1, user2, top_n=15)
                            
                            if pair_topics:
                                col1, col2 = st.columns(2)
                                with col1:
                                    topics_df = pd.DataFrame(pair_topics, columns=['Word', 'Count'])
                                    st.dataframe(topics_df, use_container_width=True)
                                
                                with col2:
                                    # Most active days for this pair
                                    active_days_pair = group_analyzer.get_most_active_days_by_pair(user1, user2, top_n=5)
                                    if not active_days_pair.empty:
                                        st.markdown("**Most Active Days Together**")
                                        st.dataframe(active_days_pair, use_container_width=True)
                            else:
                                st.info(f"Not enough interaction data between {user1} and {user2}")
                    else:
                        st.info("No significant conversation pairs found (minimum 5 interactions required)")
                    
                    st.markdown("---")
                    
                    # Reply Patterns
                    st.subheader("⏱️ Reply Patterns")
                    st.markdown("*Who responds fastest to whom?*")
                    reply_patterns = group_analyzer.get_reply_patterns()
                    
                    if not reply_patterns.empty:
                        st.dataframe(
                            reply_patterns.head(15).style.format({
                                'avg_response_time': '{:.1f} min',
                                'median_response_time': '{:.1f} min'
                            }),
                            use_container_width=True
                        )
                    else:
                        st.info("Not enough data to calculate reply patterns")
                    
                    st.markdown("---")
                    
                    # Active Time Overlap
                    st.subheader("🕒 Active Time Overlap")
                    st.markdown("*When are different users active together?*")
                    overlap = group_analyzer.get_active_time_overlap()
                    
                    if not overlap.empty:
                        st.dataframe(
                            overlap.head(10).style.format({
                                'overlap_percentage': '{:.1f}%'
                            }),
                            use_container_width=True
                        )
                    else:
                        st.info("Not enough overlap data available")
                    
                    st.markdown("---")
                    
                    # Conversation Starters
                    st.subheader("🚀 Conversation Starters")
                    st.markdown("*Who initiates conversations after long gaps?*")
                    starters = group_analyzer.get_conversation_starters()
                    
                    if not starters.empty:
                        col1, col2 = st.columns([2, 1])
                        
                        with col1:
                            st.dataframe(starters, use_container_width=True)
                        
                        with col2:
                            # Simple bar chart
                            st.bar_chart(starters.set_index('author')['conversations_started'])
                    else:
                        st.info("Not enough data to identify conversation starters")
                    
                    st.markdown("---")
                    
                    # Topics Analysis
                    st.subheader("📝 Conversation Topics")
                    topics = group_analyzer.detect_conversation_topics(min_word_length=4, top_n=15)
                    
                    # Overall topics
                    st.markdown("**Overall Most Discussed Topics**")
                    if topics['overall']:
                        topics_df = pd.DataFrame(topics['overall'], columns=['Topic', 'Count'])
                        col1, col2 = st.columns([1, 2])
                        
                        with col1:
                            st.dataframe(topics_df, use_container_width=True)
                        
                        with col2:
                            st.bar_chart(topics_df.set_index('Topic')['Count'])
                    
                    # Topics by user
                    st.markdown("**Topics by User**")
                    for user, user_topics in topics['by_user'].items():
                        if user_topics:
                            with st.expander(f"👤 {user}'s Top Topics"):
                                user_topics_df = pd.DataFrame(user_topics[:10], columns=['Topic', 'Count'])
                                st.dataframe(user_topics_df, use_container_width=True)
                    
                    # Topics by time period
                    if topics['by_period']:
                        st.markdown("**Topics Over Time (Monthly)**")
                        period_selector = st.selectbox(
                            "Select time period:",
                            list(topics['by_period'].keys())
                        )
                        
                        if period_selector:
                            period_topics = topics['by_period'][period_selector]
                            if period_topics:
                                period_df = pd.DataFrame(period_topics[:10], columns=['Topic', 'Count'])
                                st.dataframe(period_df, use_container_width=True)
            
            # Cleanup
            Path(temp_path).unlink(missing_ok=True)
            
        except Exception as e:
            st.error(f"Error processing chat file: {str(e)}")
            st.exception(e)
    
    else:
        # Show instructions when no file is uploaded
        st.info("👆 Please upload a WhatsApp chat export file to begin analysis")
        
        st.markdown("---")
        st.markdown("### 📖 How to Use")
        st.markdown("""
        1. **Export your chat** from WhatsApp (Settings → Chats → Chat History → Export Chat)
        2. **Choose 'Without Media'** when prompted
        3. **Upload the .txt file** using the sidebar
        4. **Explore the analysis** across different tabs
        
        ### 🎯 What You'll Get
        - Comprehensive user statistics and message distribution
        - Time-based activity patterns (hourly, daily, timeline)
        - Emoji usage analysis and rankings
        - Word frequency and word clouds
        - Sentiment analysis of conversations
        - Response time calculations
        """)


if __name__ == "__main__":
    main()
