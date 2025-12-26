"""
Advanced Analytics Page
"""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from src.ingestion.ingestion_service import CSVDataSource
from src.analysis.sentiment_analyzer import TrainedSentimentAnalyzer, VaderSentimentAnalyzer
from src.core.models import SentimentLabel

st.set_page_config(page_title="Analytics", page_icon="📊", layout="wide")

st.title("📊 Advanced Analytics")

# Load data function
@st.cache_data
def load_data(csv_path: str, limit: int = 1000):
    try:
        csv_source = CSVDataSource(csv_path)
        return csv_source.fetch_content(limit=limit)
    except Exception as e:
        st.error(f"Error: {e}")
        return []

@st.cache_resource
def get_analyzer():
    try:
        return TrainedSentimentAnalyzer()
    except:
        try:
            return VaderSentimentAnalyzer()
        except:
            return None

# Sidebar
csv_path = st.sidebar.text_input("CSV Path", "data/sentimentdataset.csv")
limit = st.sidebar.slider("Data Limit", 100, 5000, 1000, 100)

# Load and analyze
raw_content = load_data(csv_path, limit)
analyzer = get_analyzer()

if not raw_content or not analyzer:
    st.warning("Unable to load data or analyzer")
    st.stop()

# Analyze
analyzed = []
for content in raw_content:
    try:
        sentiment = analyzer.analyze(content.content)
        analyzed.append({
            'content': content,
            'sentiment': sentiment,
            'timestamp': content.timestamp,
            'source': content.source_type.value,
            'compound': sentiment.compound_score or 0
        })
    except:
        continue

if not analyzed:
    st.warning("No analyzed data available")
    st.stop()

# Create DataFrame
df = pd.DataFrame([{
    'timestamp': item['timestamp'],
    'source': item['source'],
    'sentiment': item['sentiment'].label.value,
    'compound': item['compound'],
    'intensity': item['sentiment'].intensity,
    'confidence': item['sentiment'].score
} for item in analyzed])

df['date'] = pd.to_datetime(df['timestamp']).dt.date
df['hour'] = pd.to_datetime(df['timestamp']).dt.hour

# Hourly analysis
st.header("⏰ Hourly Sentiment Patterns")

hourly_sentiment = df.groupby(['hour', 'sentiment']).size().reset_index(name='count')

fig_hourly = px.line(
    hourly_sentiment,
    x='hour',
    y='count',
    color='sentiment',
    title="Sentiment Distribution by Hour of Day",
    color_discrete_map={
        'positive': '#00CC96',
        'neutral': '#FFA15A',
        'negative': '#EF553B'
    }
)
st.plotly_chart(fig_hourly, use_container_width=True)

# Time vs Sentiments
st.header("⏱️ Time vs Sentiments")

# Prepare time series data with sentiment counts
df['datetime'] = pd.to_datetime(df['timestamp'])
df_sorted = df.sort_values('datetime')

# Date range filter and options
col1, col2, col3 = st.columns([2, 2, 1])

with col1:
    min_date = df_sorted['datetime'].min().date()
    max_date = df_sorted['datetime'].max().date()
    
    start_date = st.date_input(
        "Start Date",
        value=min_date,
        min_value=min_date,
        max_value=max_date,
        key="time_sentiment_start"
    )

with col2:
    end_date = st.date_input(
        "End Date",
        value=max_date,
        min_value=min_date,
        max_value=max_date,
        key="time_sentiment_end"
    )

with col3:
    time_granularity = st.selectbox(
        "Granularity",
        ["Hourly", "Daily", "Weekly"],
        index=1,
        key="time_granularity"
    )

# Filter data by date range
start_datetime = pd.Timestamp(start_date)
end_datetime = pd.Timestamp(end_date) + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)

df_filtered = df_sorted[(df_sorted['datetime'] >= start_datetime) & (df_sorted['datetime'] <= end_datetime)]

if df_filtered.empty:
    st.warning("No data available for the selected date range. Please adjust your filters.")
else:
    # Show filtered data info
    st.info(f"📊 Showing {len(df_filtered)} records from {start_date} to {end_date}")
    
    # Regroup based on selected granularity
    freq_map = {
        "Hourly": "H",
        "Daily": "D",
        "Weekly": "W"
    }
    
    time_sentiment_filtered = df_filtered.groupby([
        pd.Grouper(key='datetime', freq=freq_map[time_granularity]), 
        'sentiment'
    ]).size().reset_index(name='count')
    
    # Create enhanced line chart with better visibility
    fig_time_sentiment = go.Figure()
    
    # Add traces for each sentiment with improved styling
    sentiments = ['positive', 'neutral', 'negative']
    colors = {
        'positive': '#00CC96',
        'neutral': '#FFA15A',
        'negative': '#EF553B'
    }
    symbols = {
        'positive': 'circle',
        'neutral': 'square',
        'negative': 'diamond'
    }
    
    for sentiment in sentiments:
        sentiment_data = time_sentiment_filtered[time_sentiment_filtered['sentiment'] == sentiment]
        
        fig_time_sentiment.add_trace(go.Scatter(
            x=sentiment_data['datetime'],
            y=sentiment_data['count'],
            mode='lines+markers',
            name=sentiment.capitalize(),
            line=dict(color=colors[sentiment], width=3),
            marker=dict(
                size=8,
                symbol=symbols[sentiment],
                line=dict(width=2, color='white')
            ),
            hovertemplate='<b>%{fullData.name}</b><br>' +
                         'Time: %{x}<br>' +
                         'Count: %{y}<br>' +
                         '<extra></extra>'
        ))
    
    fig_time_sentiment.update_layout(
        title=dict(
            text=f"Sentiment Counts Over Time ({time_granularity})",
            font=dict(size=20, color='#262730')
        ),
        xaxis=dict(
            title="Timeline",
            titlefont=dict(size=14),
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(128, 128, 128, 0.2)',
            range=[start_datetime, end_datetime]
        ),
        yaxis=dict(
            title="Sentiment Count",
            titlefont=dict(size=14),
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(128, 128, 128, 0.2)'
        ),
        hovermode='x unified',
        legend=dict(
            title=dict(text="Sentiment Class", font=dict(size=12)),
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor='rgba(255, 255, 255, 0.8)',
            bordercolor='rgba(0, 0, 0, 0.2)',
            borderwidth=1
        ),
        plot_bgcolor='white',
        height=500
    )
    
    st.plotly_chart(fig_time_sentiment, use_container_width=True)
    
    # Stacked area chart for better volume visualization
    st.subheader("📊 Stacked View")
    
    fig_time_sentiment_area = px.area(
        time_sentiment_filtered,
        x='datetime',
        y='count',
        color='sentiment',
        title=f"Cumulative Sentiment Distribution ({time_granularity})",
        labels={'datetime': 'Time', 'count': 'Sentiment Count', 'sentiment': 'Sentiment'},
        color_discrete_map=colors,
        category_orders={'sentiment': ['positive', 'neutral', 'negative']}
    )
    
    fig_time_sentiment_area.update_layout(
        xaxis=dict(
            title="Timeline",
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(128, 128, 128, 0.2)',
            range=[start_datetime, end_datetime]
        ),
        yaxis=dict(
            title="Sentiment Count",
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(128, 128, 128, 0.2)'
        ),
        hovermode='x unified',
        plot_bgcolor='white',
        height=400
    )
    
    st.plotly_chart(fig_time_sentiment_area, use_container_width=True)
    
    # Summary statistics for filtered range
    col1, col2, col3, col4 = st.columns(4)
    
    sentiment_totals = time_sentiment_filtered.groupby('sentiment')['count'].sum()
    
    with col1:
        positive_count = sentiment_totals.get('positive', 0)
        st.metric("🟢 Positive", f"{positive_count:,}")
    
    with col2:
        neutral_count = sentiment_totals.get('neutral', 0)
        st.metric("🟡 Neutral", f"{neutral_count:,}")
    
    with col3:
        negative_count = sentiment_totals.get('negative', 0)
        st.metric("🔴 Negative", f"{negative_count:,}")
    
    with col4:
        total_count = sentiment_totals.sum()
        dominant = sentiment_totals.idxmax() if not sentiment_totals.empty else 'N/A'
        st.metric("📊 Total", f"{total_count:,}", f"Dominant: {dominant.capitalize()}")

# Compound score distribution
st.header("📈 Sentiment Score Distribution")

col1, col2 = st.columns(2)

with col1:
    fig_hist = px.histogram(
        df,
        x='compound',
        nbins=50,
        title="Compound Score Distribution",
        labels={'compound': 'Compound Score', 'count': 'Frequency'},
        color_discrete_sequence=['#636EFA']
    )
    st.plotly_chart(fig_hist, use_container_width=True)

with col2:
    fig_box = px.box(
        df,
        x='sentiment',
        y='compound',
        color='sentiment',
        title="Compound Score by Sentiment",
        color_discrete_map={
            'positive': '#00CC96',
            'neutral': '#FFA15A',
            'negative': '#EF553B'
        }
    )
    st.plotly_chart(fig_box, use_container_width=True)

# Confidence vs Intensity
st.header("🎯 Confidence vs Intensity Analysis")

fig_scatter = px.scatter(
    df,
    x='confidence',
    y='intensity',
    color='sentiment',
    title="Confidence vs Intensity",
    color_discrete_map={
        'positive': '#00CC96',
        'neutral': '#FFA15A',
        'negative': '#EF553B'
    },
    opacity=0.6
)
st.plotly_chart(fig_scatter, use_container_width=True)

# Source comparison
st.header("🌐 Source Comparison")

source_stats = df.groupby('source').agg({
    'compound': 'mean',
    'intensity': 'mean',
    'confidence': 'mean'
}).reset_index()

fig_source = go.Figure()
fig_source.add_trace(go.Bar(name='Avg Compound', x=source_stats['source'], y=source_stats['compound']))
fig_source.add_trace(go.Bar(name='Avg Intensity', x=source_stats['source'], y=source_stats['intensity']))
fig_source.add_trace(go.Bar(name='Avg Confidence', x=source_stats['source'], y=source_stats['confidence']))
fig_source.update_layout(title="Average Metrics by Source", barmode='group')
st.plotly_chart(fig_source, use_container_width=True)

# Daily trends
st.header("📅 Daily Trends")

daily_stats = df.groupby('date').agg({
    'compound': ['mean', 'std'],
    'sentiment': 'count'
}).reset_index()
daily_stats.columns = ['date', 'avg_compound', 'std_compound', 'count']

fig_daily = go.Figure()
fig_daily.add_trace(go.Scatter(
    x=daily_stats['date'],
    y=daily_stats['avg_compound'],
    mode='lines+markers',
    name='Avg Sentiment',
    line=dict(color='#636EFA', width=2)
))
fig_daily.add_trace(go.Bar(
    x=daily_stats['date'],
    y=daily_stats['count'],
    name='Volume',
    yaxis='y2',
    opacity=0.3
))
fig_daily.update_layout(
    title="Daily Sentiment Trend with Volume",
    yaxis=dict(title="Avg Compound Score"),
    yaxis2=dict(title="Volume", overlaying='y', side='right')
)
st.plotly_chart(fig_daily, use_container_width=True)

# Statistics summary
st.header("📊 Statistical Summary")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Compound Score")
    st.write(f"Mean: {df['compound'].mean():.3f}")
    st.write(f"Median: {df['compound'].median():.3f}")
    st.write(f"Std Dev: {df['compound'].std():.3f}")

with col2:
    st.subheader("Intensity")
    st.write(f"Mean: {df['intensity'].mean():.3f}")
    st.write(f"Median: {df['intensity'].median():.3f}")
    st.write(f"Std Dev: {df['intensity'].std():.3f}")

with col3:
    st.subheader("Confidence")
    st.write(f"Mean: {df['confidence'].mean():.3f}")
    st.write(f"Median: {df['confidence'].median():.3f}")
    st.write(f"Std Dev: {df['confidence'].std():.3f}")
