"""
Streamlit dashboard application.
Single Responsibility: Visualize data and insights.
"""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta
from collections import Counter
import os
import sys

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.ingestion.ingestion_service import CSVDataSource
from src.analysis.sentiment_analyzer import TrainedSentimentAnalyzer, VaderSentimentAnalyzer
from src.core.models import SourceType, SentimentLabel


# Page config
st.set_page_config(
    page_title="Vibe Optimizer Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data(csv_path: str, limit: int = 1000):
    """Load data from CSV file."""
    try:
        csv_source = CSVDataSource(csv_path)
        content = csv_source.fetch_content(limit=limit)
        return content
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return []


@st.cache_resource
def get_sentiment_analyzer():
    """Initialize sentiment analyzer."""
    try:
        # Try trained model first
        analyzer = TrainedSentimentAnalyzer()
        return analyzer
    except:
        # Fallback to VADER
        try:
            return VaderSentimentAnalyzer()
        except:
            return None


def analyze_content(content_list, analyzer):
    """Analyze sentiment for content."""
    results = []
    for content in content_list:
        try:
            sentiment = analyzer.analyze(content.content)
            results.append({
                'content': content,
                'sentiment': sentiment
            })
        except Exception as e:
            continue
    return results


def filter_by_date(content_list, start_date, end_date):
    """Filter content by date range."""
    start_dt = datetime.combine(start_date, datetime.min.time())
    end_dt = datetime.combine(end_date, datetime.max.time())
    
    return [c for c in content_list if start_dt <= c.timestamp <= end_dt]


def filter_by_source(content_list, sources):
    """Filter content by source types."""
    if not sources:
        return content_list
    
    source_map = {
        'Twitter': SourceType.TWITTER,
        'Reddit': SourceType.REDDIT,
        'Reviews': SourceType.REVIEWS
    }
    
    selected_types = [source_map[s] for s in sources if s in source_map]
    return [c for c in content_list if c.source_type in selected_types]


def calculate_metrics(analyzed_data):
    """Calculate dashboard metrics."""
    if not analyzed_data:
        return {
            'total': 0,
            'positive': 0,
            'neutral': 0,
            'negative': 0,
            'avg_score': 0,
            'avg_intensity': 0
        }
    
    sentiments = [item['sentiment'] for item in analyzed_data]
    
    positive = sum(1 for s in sentiments if s.label == SentimentLabel.POSITIVE)
    neutral = sum(1 for s in sentiments if s.label == SentimentLabel.NEUTRAL)
    negative = sum(1 for s in sentiments if s.label == SentimentLabel.NEGATIVE)
    
    avg_score = sum(s.score for s in sentiments) / len(sentiments)
    avg_intensity = sum(s.intensity for s in sentiments) / len(sentiments)
    
    return {
        'total': len(analyzed_data),
        'positive': positive,
        'neutral': neutral,
        'negative': negative,
        'avg_score': avg_score,
        'avg_intensity': avg_intensity
    }


def main():
    st.title("📊 Vibe Optimizer Dashboard")
    st.markdown("Real-time brand sentiment and insights")
    
    # Sidebar
    st.sidebar.header("⚙️ Configuration")
    
    # Data source selection
    csv_path = st.sidebar.text_input(
        "CSV Data Path",
        value="data/sentimentdataset.csv"
    )
    
    data_limit = st.sidebar.slider(
        "Data Limit",
        min_value=100,
        max_value=5000,
        value=1000,
        step=100
    )
    
    st.sidebar.header("🔍 Filters")
    
    # Date range filter
    col1, col2 = st.sidebar.columns(2)
    with col1:
        start_date = st.date_input(
            "Start Date",
            value=datetime.now() - timedelta(days=30)
        )
    with col2:
        end_date = st.date_input(
            "End Date",
            value=datetime.now()
        )
    
    # Source filter
    source_filter = st.sidebar.multiselect(
        "Data Sources",
        ["Twitter", "Reddit", "Reviews"],
        default=["Twitter", "Reddit"]
    )
    
    # Search filter
    search_query = st.sidebar.text_input(
        "Search Keywords",
        placeholder="Enter keywords to filter..."
    )
    
    # Load data
    with st.spinner("Loading data..."):
        raw_content = load_data(csv_path, data_limit)
    
    if not raw_content:
        st.warning("No data loaded. Please check the CSV path.")
        return
    
    # Apply filters
    filtered_content = filter_by_date(raw_content, start_date, end_date)
    filtered_content = filter_by_source(filtered_content, source_filter)
    
    if search_query:
        filtered_content = [
            c for c in filtered_content 
            if search_query.lower() in c.content.lower()
        ]
    
    st.sidebar.metric("Filtered Records", len(filtered_content))
    
    # Initialize analyzer
    analyzer = get_sentiment_analyzer()
    
    if analyzer is None:
        st.error("Could not initialize sentiment analyzer. Please check model files.")
        return
    
    # Analyze content
    with st.spinner("Analyzing sentiment..."):
        analyzed_data = analyze_content(filtered_content, analyzer)
    
    # Check if we have any analyzed data
    if not analyzed_data:
        st.warning("⚠️ No data available after filtering. Please adjust your filters or check the data source.")
        st.info("💡 Tips:\n- Increase the data limit\n- Expand the date range\n- Remove source filters\n- Clear search keywords")
        return
    
    # Calculate metrics
    metrics = calculate_metrics(analyzed_data)
    
    # Display metrics
    st.header("📈 Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        sentiment_label = "Positive" if metrics['positive'] > metrics['negative'] else \
                         "Negative" if metrics['negative'] > metrics['positive'] else "Neutral"
        sentiment_color = "🟢" if sentiment_label == "Positive" else \
                         "🔴" if sentiment_label == "Negative" else "🟡"
        st.metric(
            "Overall Sentiment",
            f"{sentiment_color} {sentiment_label}",
            f"{metrics['positive']} positive"
        )
    
    with col2:
        st.metric(
            "Total Mentions",
            f"{metrics['total']:,}",
            f"{metrics['positive'] + metrics['negative']} with sentiment"
        )
    
    with col3:
        st.metric(
            "Avg Confidence",
            f"{metrics['avg_score']:.2%}",
            f"Intensity: {metrics['avg_intensity']:.2f}"
        )
    
    with col4:
        positive_pct = (metrics['positive'] / metrics['total'] * 100) if metrics['total'] > 0 else 0
        st.metric(
            "Positive Rate",
            f"{positive_pct:.1f}%",
            f"{metrics['negative']} negative"
        )
    
    # Sentiment distribution
    st.header("📊 Sentiment Distribution")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Pie chart
        sentiment_df = pd.DataFrame({
            'Sentiment': ['Positive', 'Neutral', 'Negative'],
            'Count': [metrics['positive'], metrics['neutral'], metrics['negative']],
            'Color': ['#00CC96', '#FFA15A', '#EF553B']
        })
        
        fig_pie = px.pie(
            sentiment_df,
            values='Count',
            names='Sentiment',
            color='Sentiment',
            color_discrete_map={
                'Positive': '#00CC96',
                'Neutral': '#FFA15A',
                'Negative': '#EF553B'
            },
            title="Sentiment Breakdown"
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        st.subheader("Distribution")
        if metrics['total'] > 0:
            st.write(f"**Positive:** {metrics['positive']} ({metrics['positive']/metrics['total']*100:.1f}%)")
            st.write(f"**Neutral:** {metrics['neutral']} ({metrics['neutral']/metrics['total']*100:.1f}%)")
            st.write(f"**Negative:** {metrics['negative']} ({metrics['negative']/metrics['total']*100:.1f}%)")
        else:
            st.write("**Positive:** 0 (0.0%)")
            st.write("**Neutral:** 0 (0.0%)")
            st.write("**Negative:** 0 (0.0%)")
        st.write("---")
        st.write(f"**Total:** {metrics['total']}")
    
    # Sentiment over time
    st.header("📈 Sentiment Trend Over Time")
    
    if analyzed_data:
        # Create time series data
        time_data = []
        for item in analyzed_data:
            time_data.append({
                'timestamp': item['content'].timestamp,
                'sentiment': item['sentiment'].label.value,
                'score': item['sentiment'].compound_score or 0
            })
        
        time_df = pd.DataFrame(time_data)
        time_df['date'] = pd.to_datetime(time_df['timestamp']).dt.date
        
        # Aggregate by date
        daily_sentiment = time_df.groupby(['date', 'sentiment']).size().reset_index(name='count')
        
        fig_line = px.line(
            daily_sentiment,
            x='date',
            y='count',
            color='sentiment',
            color_discrete_map={
                'positive': '#00CC96',
                'neutral': '#FFA15A',
                'negative': '#EF553B'
            },
            title="Daily Sentiment Counts",
            labels={'count': 'Number of Mentions', 'date': 'Date'}
        )
        st.plotly_chart(fig_line, use_container_width=True)
        
        # Compound score over time
        daily_compound = time_df.groupby('date')['score'].mean().reset_index()
        
        fig_compound = go.Figure()
        fig_compound.add_trace(go.Scatter(
            x=daily_compound['date'],
            y=daily_compound['score'],
            mode='lines+markers',
            name='Avg Sentiment Score',
            line=dict(color='#636EFA', width=3),
            fill='tozeroy'
        ))
        fig_compound.update_layout(
            title="Average Sentiment Score Over Time",
            xaxis_title="Date",
            yaxis_title="Compound Score (-1 to 1)",
            hovermode='x unified'
        )
        st.plotly_chart(fig_compound, use_container_width=True)
    
    # Source breakdown
    st.header("🌐 Source Analysis")
    col1, col2 = st.columns(2)
    
    with col1:
        # Source distribution
        source_counts = Counter([c.source_type.value for c in filtered_content])
        source_df = pd.DataFrame({
            'Source': list(source_counts.keys()),
            'Count': list(source_counts.values())
        })
        
        fig_source = px.bar(
            source_df,
            x='Source',
            y='Count',
            title="Mentions by Source",
            color='Source'
        )
        st.plotly_chart(fig_source, use_container_width=True)
    
    with col2:
        # Sentiment by source
        if analyzed_data:
            source_sentiment = []
            for item in analyzed_data:
                source_sentiment.append({
                    'source': item['content'].source_type.value,
                    'sentiment': item['sentiment'].label.value
                })
            
            source_sent_df = pd.DataFrame(source_sentiment)
            source_sent_counts = source_sent_df.groupby(['source', 'sentiment']).size().reset_index(name='count')
            
            fig_source_sent = px.bar(
                source_sent_counts,
                x='source',
                y='count',
                color='sentiment',
                title="Sentiment by Source",
                color_discrete_map={
                    'positive': '#00CC96',
                    'neutral': '#FFA15A',
                    'negative': '#EF553B'
                },
                barmode='group'
            )
            st.plotly_chart(fig_source_sent, use_container_width=True)
    
    # Top keywords/hashtags
    st.header("🔤 Top Keywords")
    
    if filtered_content:
        # Extract hashtags from metadata
        all_hashtags = []
        for content in filtered_content:
            hashtags = content.metadata.get('hashtags', '')
            if hashtags:
                all_hashtags.extend([h.strip() for h in str(hashtags).split(',') if h.strip()])
        
        if all_hashtags:
            hashtag_counts = Counter(all_hashtags).most_common(10)
            hashtag_df = pd.DataFrame(hashtag_counts, columns=['Hashtag', 'Count'])
            
            fig_hashtags = px.bar(
                hashtag_df,
                x='Count',
                y='Hashtag',
                orientation='h',
                title="Top 10 Hashtags",
                color='Count',
                color_continuous_scale='Blues'
            )
            st.plotly_chart(fig_hashtags, use_container_width=True)
        else:
            st.info("No hashtags found in the data.")
    
    # Recent mentions
    st.header("💬 Recent Mentions")
    
    sentiment_filter = st.selectbox(
        "Filter by Sentiment",
        ["All", "Positive", "Neutral", "Negative"]
    )
    
    # Filter analyzed data
    display_data = analyzed_data
    if sentiment_filter != "All":
        display_data = [
            item for item in analyzed_data 
            if item['sentiment'].label.value == sentiment_filter.lower()
        ]
    
    # Display recent mentions
    num_display = st.slider("Number of mentions to display", 5, 50, 10)
    
    for i, item in enumerate(display_data[:num_display]):
        content = item['content']
        sentiment = item['sentiment']
        
        # Sentiment emoji
        emoji = "🟢" if sentiment.label == SentimentLabel.POSITIVE else \
                "🔴" if sentiment.label == SentimentLabel.NEGATIVE else "🟡"
        
        with st.expander(f"{emoji} {content.content[:100]}... - {content.timestamp.strftime('%Y-%m-%d %H:%M')}"):
            st.write(f"**Full Text:** {content.content}")
            st.write(f"**Source:** {content.source_type.value.title()}")
            st.write(f"**Author:** {content.author or 'Unknown'}")
            st.write(f"**Timestamp:** {content.timestamp}")
            st.write("---")
            st.write(f"**Sentiment:** {sentiment.label.value.title()}")
            st.write(f"**Confidence:** {sentiment.score:.2%}")
            st.write(f"**Intensity:** {sentiment.intensity:.2f}")
            if sentiment.compound_score is not None:
                st.write(f"**Compound Score:** {sentiment.compound_score:.2f}")
            
            # Metadata
            if content.metadata:
                st.write("**Metadata:**")
                for key, value in content.metadata.items():
                    if value and key not in ['sentiment']:
                        st.write(f"  - {key}: {value}")
    
    # Footer
    st.markdown("---")
    st.markdown("*Vibe Optimizer Dashboard - Powered by Streamlit*")


if __name__ == "__main__":
    main()
