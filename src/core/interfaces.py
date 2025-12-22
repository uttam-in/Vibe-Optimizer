"""
Abstract interfaces for dependency inversion.
Dependency Inversion Principle: Depend on abstractions, not concretions.
Interface Segregation Principle: Focused, specific interfaces.
"""
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from datetime import datetime

from .models import (
    RawContent, AnalyzedContent, SentimentScore, 
    Topic, Insight, SentimentTrend, SourceType
)


class IDataSource(ABC):
    """
    Interface for data ingestion sources.
    Open/Closed: New sources can be added without modifying existing code.
    """
    
    @abstractmethod
    def fetch_content(
        self, 
        query: str, 
        since: Optional[datetime] = None,
        limit: int = 100
    ) -> List[RawContent]:
        """Fetch content from the source."""
        pass
    
    @abstractmethod
    def get_source_type(self) -> SourceType:
        """Return the source type identifier."""
        pass


class ISentimentAnalyzer(ABC):
    """Interface for sentiment analysis."""
    
    @abstractmethod
    def analyze(self, text: str) -> SentimentScore:
        """Analyze sentiment of given text."""
        pass


class ITopicExtractor(ABC):
    """Interface for topic extraction and clustering."""
    
    @abstractmethod
    def extract_topics(self, texts: List[str], num_topics: int = 5) -> List[Topic]:
        """Extract topics from a collection of texts."""
        pass
    
    @abstractmethod
    def assign_topics(self, text: str, topics: List[Topic]) -> List[Topic]:
        """Assign relevant topics to a single text."""
        pass


class IRepository(ABC):
    """
    Generic repository interface for data persistence.
    Single Responsibility: Handle data storage operations.
    """
    
    @abstractmethod
    def save(self, entity: Any) -> str:
        """Save an entity and return its ID."""
        pass
    
    @abstractmethod
    def get_by_id(self, entity_id: str) -> Optional[Any]:
        """Retrieve entity by ID."""
        pass
    
    @abstractmethod
    def find(self, filters: Dict[str, Any]) -> List[Any]:
        """Find entities matching filters."""
        pass
    
    @abstractmethod
    def delete(self, entity_id: str) -> bool:
        """Delete an entity."""
        pass


class IInsightGenerator(ABC):
    """Interface for generating business insights."""
    
    @abstractmethod
    def generate_insights(
        self, 
        analyzed_content: List[AnalyzedContent],
        time_window: Optional[tuple[datetime, datetime]] = None
    ) -> List[Insight]:
        """Generate insights from analyzed content."""
        pass


class IReportGenerator(ABC):
    """Interface for report generation."""
    
    @abstractmethod
    def generate_report(
        self,
        start_date: datetime,
        end_date: datetime,
        format: str = "html"
    ) -> str:
        """Generate a report for the given period."""
        pass


class INotificationService(ABC):
    """Interface for sending notifications."""
    
    @abstractmethod
    def send_email(
        self,
        to: List[str],
        subject: str,
        body: str,
        attachments: Optional[List[str]] = None
    ) -> bool:
        """Send email notification."""
        pass
