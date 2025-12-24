"""
Example dashboard components for sentiment analysis visualization.
Ready for Streamlit integration.
"""
import pandas as pd
from typing import List, Dict
from datetime import datetime, timedelta

from src.analysis.sentiment_analyzer import TrainedSentimentAnalyzer
from src.ingestion.ingestion_service import CSVDataSource
from src.core.models import SourceType, RawContent


class SentimentDashboardData:
    """
    Data provider for sentiment analysis dashboard.
    Prepares data for visualization.
    """
    
    def __init__(self, model_path: str = "models/sentiment_model.pkl"):
        """
        Initialize dashboard data provider.
        
        Args:
            model_path: Path to trained model
        """
        self.analyzer = TrainedSentimentAnalyzer(model_path=model_path)
    
    def analyze_dataset(
        self, 
        csv_path: str, 
        limit: int = None
    ) -> pd.DataFrame:
        """
        Analyze dataset and return results as DataFrame.
        
        Args:
            csv_path: Path to CSV dataset
            limit: Maximum number of items to analyze
            
        Returns:
            DataFrame with analysis results
        """
        # Load data
        csv_source = CSVDataSource(csv_path)
        raw_content = csv_source.fetch_content(query="", limit=limit or 1000)
        
        # Analyze each item
        results = []
        for item in raw_content:
            sentiment = self.analyzer.analyze(item.content)
            
            results.append({
                'id': item.id,
                'text': item.content,
                'author': item.author,
                'timestamp': item.timestamp,
                'source': item.source_type.value,
                'predicted_sentiment': sentiment.label.value,
                'confidence': sentiment.score,
                'intensity': sentiment.intensity,
                'compound_score': sentiment.compound_score,
                'original_sentiment': item.metadata.get('sentiment', '').strip().lower(),
                'platform': item.metadata.get('platform', ''),
                'likes': item.metadata.get('likes', 0),
                'retweets': item.metadata.get('retweets', 0),
                'country': item.metadata.get('country', '')
            })
        
        return pd.DataFrame(results)
    
    def get_sentiment_distribution(self, df: pd.DataFrame) -> Dict[str, int]:
        """Get sentiment distribution counts."""
        return df['predicted_sentiment'].value_counts().to_dict()
    
    def get_sentiment_over_time(
        self, 
        df: pd.DataFrame, 
        freq: str = 'D'
    ) -> pd.DataFrame:
        """
        Get sentiment distribution over time.
        
        Args:
            df: Analysis results DataFrame
            freq: Frequency for grouping ('D'=daily, 'W'=weekly, 'M'=monthly)
            
        Returns:
            DataFrame with sentiment counts over time
        """
        df['date'] = pd.to_datetime(df['timestamp'])
        
        # Group by date and sentiment
        sentiment_time = df.groupby([
            pd.Grouper(key='date', freq=freq),
            'predicted_sentiment'
        ]).size().unstack(fill_value=0)
        
        return sentiment_time
    
    def get_average_metrics(self, df: pd.DataFrame) -> Dict[str, float]:
        """Get average sentiment metrics."""
        return {
            'avg_confidence': df['confidence'].mean(),
            'avg_intensity': df['intensity'].mean(),
            'avg_compound_score': df['compound_score'].mean(),
            'total_analyzed': len(df)
        }
    
    def get_top_positive_texts(self, df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
        """Get top N most positive texts."""
        positive = df[df['predicted_sentiment'] == 'positive']
        return positive.nlargest(n, 'compound_score')[
            ['text', 'compound_score', 'confidence', 'timestamp']
        ]
    
    def get_top_negative_texts(self, df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
        """Get top N most negative texts."""
        negative = df[df['predicted_sentiment'] == 'negative']
        return negative.nsmallest(n, 'compound_score')[
            ['text', 'compound_score', 'confidence', 'timestamp']
        ]
    
    def get_sentiment_by_source(self, df: pd.DataFrame) -> pd.DataFrame:
        """Get sentiment distribution by source/platform."""
        return pd.crosstab(
            df['platform'], 
            df['predicted_sentiment'],
            normalize='index'
        ) * 100
    
    def get_model_accuracy(self, df: pd.DataFrame) -> Dict[str, float]:
        """
        Calculate model accuracy against original labels.
        
        Args:
            df: DataFrame with both predicted and original sentiments
            
        Returns:
            Accuracy metrics
        """
        # Filter rows with valid original labels
        valid = df[df['original_sentiment'].isin(['positive', 'negative', 'neutral'])]
        
        if len(valid) == 0:
            return {'accuracy': 0.0, 'total_compared': 0}
        
        # Calculate accuracy
        matches = (valid['predicted_sentiment'] == valid['original_sentiment']).sum()
        accuracy = matches / len(valid)
        
        return {
            'accuracy': accuracy,
            'total_compared': len(valid),
            'matches': matches
        }


# Streamlit Dashboard Example
"""
To create a Streamlit dashboard, create a file like dashboard_app.py:

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from src.dashboard.sentiment_dashboard_example import SentimentDashboardData

# Page config
st.set_page_config(
    page_title="Sentiment Analysis Dashboard",
    page_icon="📊",
    layout="wide"
)

# Title
st.title("📊 Sentiment Analysis Dashboard")

# Initialize data provider
@st.cache_resource
def load_analyzer():
    return SentimentDashboardData(model_path="models/sentiment_model.pkl")

dashboard = load_analyzer()

# Sidebar
st.sidebar.header("Settings")
csv_path = st.sidebar.text_input("Dataset Path", "data/sentimentdataset.csv")
limit = st.sidebar.slider("Number of samples", 10, 500, 100)

# Load and analyze data
if st.sidebar.button("Analyze Dataset"):
    with st.spinner("Analyzing dataset..."):
        df = dashboard.analyze_dataset(csv_path, limit=limit)
        st.session_state['df'] = df

# Display results
if 'df' in st.session_state:
    df = st.session_state['df']
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    metrics = dashboard.get_average_metrics(df)
    
    with col1:
        st.metric("Total Analyzed", metrics['total_analyzed'])
    with col2:
        st.metric("Avg Confidence", f"{metrics['avg_confidence']:.3f}")
    with col3:
        st.metric("Avg Intensity", f"{metrics['avg_intensity']:.3f}")
    with col4:
        st.metric("Avg Compound", f"{metrics['avg_compound_score']:.3f}")
    
    # Sentiment Distribution
    st.subheader("Sentiment Distribution")
    dist = dashboard.get_sentiment_distribution(df)
    fig = px.pie(
        values=list(dist.values()),
        names=list(dist.keys()),
        title="Sentiment Distribution"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Sentiment Over Time
    st.subheader("Sentiment Over Time")
    time_data = dashboard.get_sentiment_over_time(df, freq='D')
    fig = px.line(
        time_data,
        title="Sentiment Trends Over Time"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Top Positive/Negative
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Top Positive Texts")
        top_pos = dashboard.get_top_positive_texts(df, n=5)
        st.dataframe(top_pos)
    
    with col2:
        st.subheader("Top Negative Texts")
        top_neg = dashboard.get_top_negative_texts(df, n=5)
        st.dataframe(top_neg)
    
    # Model Accuracy
    st.subheader("Model Performance")
    accuracy = dashboard.get_model_accuracy(df)
    st.metric("Accuracy", f"{accuracy['accuracy']:.2%}")
    st.write(f"Compared {accuracy['total_compared']} samples")

Run with: streamlit run dashboard_app.py
"""
