"""
Utility functions for the dashboard
"""
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from collections import Counter

from src.core.models import RawContent, SentimentScore, SentimentLabel


def format_timestamp(dt: datetime, format: str = "%Y-%m-%d %H:%M") -> str:
    """Format datetime for display"""
    return dt.strftime(format)


def calculate_sentiment_distribution(analyzed_data: List[Dict]) -> Dict[str, int]:
    """Calculate sentiment distribution from analyzed data"""
    distribution = {
        'positive': 0,
        'neutral': 0,
        'negative': 0
    }
    
    for item in analyzed_data:
        sentiment = item['sentiment']
        label = sentiment.label.value
        distribution[label] = distribution.get(label, 0) + 1
    
    return distribution


def calculate_change_percentage(current: float, previous: float) -> Optional[float]:
    """Calculate percentage change"""
    if previous == 0:
        return None
    return ((current - previous) / previous) * 100


def get_sentiment_emoji(label: SentimentLabel) -> str:
    """Get emoji for sentiment label"""
    emoji_map = {
        SentimentLabel.POSITIVE: "🟢",
        SentimentLabel.NEUTRAL: "🟡",
        SentimentLabel.NEGATIVE: "🔴"
    }
    return emoji_map.get(label, "⚪")


def extract_hashtags(content_list: List[RawContent]) -> List[tuple]:
    """Extract and count hashtags from content"""
    all_hashtags = []
    
    for content in content_list:
        hashtags = content.metadata.get('hashtags', '')
        if hashtags:
            tags = [h.strip() for h in str(hashtags).split(',') if h.strip()]
            all_hashtags.extend(tags)
    
    return Counter(all_hashtags).most_common(20)


def create_time_series_df(analyzed_data: List[Dict]) -> pd.DataFrame:
    """Create time series DataFrame from analyzed data"""
    time_data = []
    
    for item in analyzed_data:
        time_data.append({
            'timestamp': item['content'].timestamp,
            'sentiment': item['sentiment'].label.value,
            'score': item['sentiment'].score,
            'compound': item['sentiment'].compound_score or 0,
            'intensity': item['sentiment'].intensity,
            'source': item['content'].source_type.value
        })
    
    df = pd.DataFrame(time_data)
    df['date'] = pd.to_datetime(df['timestamp']).dt.date
    df['hour'] = pd.to_datetime(df['timestamp']).dt.hour
    
    return df


def aggregate_by_period(df: pd.DataFrame, period: str = 'D') -> pd.DataFrame:
    """Aggregate sentiment data by time period"""
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.set_index('timestamp')
    
    # Resample by period
    aggregated = df.groupby([pd.Grouper(freq=period), 'sentiment']).size().reset_index(name='count')
    
    return aggregated


def calculate_sentiment_score(positive: int, neutral: int, negative: int) -> float:
    """Calculate overall sentiment score (0-10)"""
    total = positive + neutral + negative
    if total == 0:
        return 5.0
    
    # Weighted score: positive=10, neutral=5, negative=0
    score = (positive * 10 + neutral * 5 + negative * 0) / total
    return round(score, 1)


def get_top_authors(content_list: List[RawContent], limit: int = 10) -> List[tuple]:
    """Get top authors by post count"""
    authors = [c.author for c in content_list if c.author]
    return Counter(authors).most_common(limit)


def filter_by_sentiment(analyzed_data: List[Dict], sentiment: str) -> List[Dict]:
    """Filter analyzed data by sentiment label"""
    if sentiment.lower() == 'all':
        return analyzed_data
    
    return [
        item for item in analyzed_data 
        if item['sentiment'].label.value == sentiment.lower()
    ]


def get_sentiment_trend(df: pd.DataFrame, window: int = 7) -> pd.DataFrame:
    """Calculate moving average sentiment trend"""
    df = df.copy()
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.sort_values('timestamp')
    
    # Calculate rolling average of compound score
    df['trend'] = df['compound'].rolling(window=window, min_periods=1).mean()
    
    return df


def export_to_csv(analyzed_data: List[Dict]) -> str:
    """Export analyzed data to CSV string"""
    export_data = []
    
    for item in analyzed_data:
        content = item['content']
        sentiment = item['sentiment']
        
        export_data.append({
            'Timestamp': content.timestamp,
            'Source': content.source_type.value,
            'Author': content.author or '',
            'Content': content.content,
            'Sentiment': sentiment.label.value,
            'Confidence': sentiment.score,
            'Intensity': sentiment.intensity,
            'Compound_Score': sentiment.compound_score or 0
        })
    
    df = pd.DataFrame(export_data)
    return df.to_csv(index=False)


def get_peak_hours(df: pd.DataFrame) -> List[int]:
    """Get peak hours for mentions"""
    hourly_counts = df.groupby('hour').size()
    top_hours = hourly_counts.nlargest(3).index.tolist()
    return sorted(top_hours)


def calculate_engagement_metrics(content_list: List[RawContent]) -> Dict[str, float]:
    """Calculate engagement metrics from metadata"""
    total_likes = 0
    total_retweets = 0
    count = 0
    
    for content in content_list:
        likes = content.metadata.get('likes')
        retweets = content.metadata.get('retweets')
        
        if likes is not None:
            total_likes += float(likes)
            count += 1
        
        if retweets is not None:
            total_retweets += float(retweets)
    
    return {
        'avg_likes': total_likes / count if count > 0 else 0,
        'avg_retweets': total_retweets / count if count > 0 else 0,
        'total_likes': total_likes,
        'total_retweets': total_retweets
    }


def detect_sentiment_shift(df: pd.DataFrame, threshold: float = 0.2) -> Optional[Dict]:
    """Detect significant sentiment shifts"""
    if len(df) < 2:
        return None
    
    df = df.sort_values('timestamp')
    
    # Compare first half vs second half
    mid_point = len(df) // 2
    first_half = df.iloc[:mid_point]['compound'].mean()
    second_half = df.iloc[mid_point:]['compound'].mean()
    
    change = second_half - first_half
    
    if abs(change) >= threshold:
        return {
            'detected': True,
            'direction': 'positive' if change > 0 else 'negative',
            'magnitude': abs(change),
            'first_half_avg': first_half,
            'second_half_avg': second_half
        }
    
    return None


def format_large_number(num: int) -> str:
    """Format large numbers with K, M suffixes"""
    if num >= 1_000_000:
        return f"{num/1_000_000:.1f}M"
    elif num >= 1_000:
        return f"{num/1_000:.1f}K"
    else:
        return str(num)
