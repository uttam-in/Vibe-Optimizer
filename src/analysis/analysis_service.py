"""
Analysis orchestration service.
Single Responsibility: Coordinate NLP analysis pipeline.
Dependency Inversion: Depends on analyzer interfaces.
"""
from typing import List
from datetime import datetime

from src.core.interfaces import ISentimentAnalyzer, ITopicExtractor, IRepository
from src.core.models import RawContent, AnalyzedContent, Topic


class AnalysisService:
    """Orchestrates NLP analysis pipeline."""
    
    def __init__(
        self,
        sentiment_analyzer: ISentimentAnalyzer,
        topic_extractor: ITopicExtractor,
        repository: IRepository
    ):
        self.sentiment_analyzer = sentiment_analyzer
        self.topic_extractor = topic_extractor
        self.repository = repository
    
    def analyze_content(self, raw_content: List[RawContent]) -> List[AnalyzedContent]:
        """
        Run full analysis pipeline on raw content.
        
        Args:
            raw_content: List of raw content to analyze
            
        Returns:
            List of analyzed content with sentiment and topics
        """
        # Extract topics from all content first
        all_texts = [c.content for c in raw_content]
        topics = self.topic_extractor.extract_topics(all_texts)
        
        analyzed = []
        for content in raw_content:
            # Analyze sentiment
            sentiment = self.sentiment_analyzer.analyze(content.content)
            
            # Assign topics
            assigned_topics = self.topic_extractor.assign_topics(
                content.content, 
                topics
            )
            
            # Extract entities (placeholder)
            entities = self._extract_entities(content.content)
            
            analyzed_item = AnalyzedContent(
                raw_content=content,
                sentiment=sentiment,
                topics=assigned_topics,
                entities=entities,
                processed_at=datetime.now()
            )
            
            # Save to repository
            self.repository.save(analyzed_item)
            analyzed.append(analyzed_item)
        
        return analyzed
    
    def _extract_entities(self, text: str) -> List[str]:
        """Extract named entities from text."""
        # Implementation: Use spaCy NER
        pass
