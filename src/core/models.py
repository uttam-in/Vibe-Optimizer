"""
Core domain models representing business entities.
Single Responsibility: Each model represents one domain concept.
"""
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional, List, Dict, Any


class SentimentLabel(Enum):
    """Sentiment classification labels."""
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"


class SourceType(Enum):
    """Supported data source types."""
    TWITTER = "twitter"
    REDDIT = "reddit"
    REVIEWS = "reviews"
    SUPPORT_TICKETS = "support_tickets"
    FORUMS = "forums"


@dataclass
class RawContent:
    """Raw content ingested from external sources."""
    id: str
    source_type: SourceType
    content: str
    author: Optional[str]
    timestamp: datetime
    metadata: Dict[str, Any]
    url: Optional[str] = None


@dataclass
class SentimentScore:
    """Sentiment analysis result."""
    label: SentimentLabel
    score: float  # Confidence score 0-1
    intensity: float  # Sentiment intensity 0-1
    compound_score: Optional[float] = None  # Overall sentiment -1 to 1


@dataclass
class Topic:
    """Identified topic/theme."""
    id: str
    name: str
    keywords: List[str]
    relevance_score: float


@dataclass
class AnalyzedContent:
    """Content after NLP analysis."""
    raw_content: RawContent
    sentiment: SentimentScore
    topics: List[Topic]
    entities: List[str]
    processed_at: datetime


@dataclass
class Insight:
    """Generated business insight."""
    id: str
    title: str
    description: str
    insight_type: str  # 'trend', 'risk', 'opportunity', 'complaint'
    severity: str  # 'low', 'medium', 'high', 'critical'
    supporting_data: Dict[str, Any]
    created_at: datetime
    actionable_recommendations: List[str]


@dataclass
class SentimentTrend:
    """Sentiment trend over time."""
    period_start: datetime
    period_end: datetime
    sentiment_distribution: Dict[SentimentLabel, int]
    average_intensity: float
    total_mentions: int
    change_percentage: Optional[float] = None
