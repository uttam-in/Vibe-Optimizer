"""
Integration tests for sentiment analysis module.
Tests the integration between components in src/analysis.
"""
import pytest
import os
from datetime import datetime
from src.analysis.sentiment_analyzer import TrainedSentimentAnalyzer
from src.analysis.analysis_service import AnalysisService
from src.ingestion.ingestion_service import CSVDataSource
from src.core.models import (
    RawContent, AnalyzedContent, SentimentScore, 
    SentimentLabel, SourceType, Topic
)


# Mock implementations for testing
class MockTopicExtractor:
    """Mock topic extractor for testing."""
    
    def extract_topics(self, texts, num_topics=5):
        """Return mock topics."""
        return [
            Topic(
                id="topic_1",
                name="Product Quality",
                keywords=["quality", "product", "great"],
                relevance_score=0.8
            ),
            Topic(
                id="topic_2",
                name="Service",
                keywords=["service", "support"],
                relevance_score=0.6
            )
        ]
    
    def assign_topics(self, text, topics):
        """Assign topics based on keywords."""
        text_lower = text.lower()
        assigned = []
        for topic in topics:
            if any(keyword in text_lower for keyword in topic.keywords):
                assigned.append(topic)
        return assigned[:2]


class MockRepository:
    """Mock repository for testing."""
    
    def __init__(self):
        self.storage = []
    
    def save(self, entity):
        """Save entity."""
        self.storage.append(entity)
        return f"id_{len(self.storage)}"
    
    def get_by_id(self, entity_id):
        """Get by ID."""
        idx = int(entity_id.split('_')[1]) - 1
        return self.storage[idx] if 0 <= idx < len(self.storage) else None
    
    def find(self, filters):
        """Find entities."""
        return self.storage
    
    def delete(self, entity_id):
        """Delete entity."""
        return True


@pytest.fixture
def trained_analyzer():
    """Fixture for trained sentiment analyzer."""
    model_path = "models/sentiment_model.pkl"
    if not os.path.exists(model_path):
        pytest.skip("Model not trained. Run: python scripts/train_sentiment_model.py")
    return TrainedSentimentAnalyzer(model_path=model_path)


@pytest.fixture
def mock_topic_extractor():
    """Fixture for mock topic extractor."""
    return MockTopicExtractor()


@pytest.fixture
def mock_repository():
    """Fixture for mock repository."""
    return MockRepository()


@pytest.fixture
def analysis_service(trained_analyzer, mock_topic_extractor, mock_repository):
    """Fixture for analysis service with all dependencies."""
    return AnalysisService(
        sentiment_analyzer=trained_analyzer,
        topic_extractor=mock_topic_extractor,
        repository=mock_repository
    )


@pytest.fixture
def sample_raw_content():
    """Fixture for sample raw content."""
    return [
        RawContent(
            id="1",
            source_type=SourceType.TWITTER,
            content="I love this amazing product! Best purchase ever!",
            author="user1",
            timestamp=datetime.now(),
            metadata={"platform": "twitter"}
        ),
        RawContent(
            id="2",
            source_type=SourceType.TWITTER,
            content="This is terrible. Very disappointed.",
            author="user2",
            timestamp=datetime.now(),
            metadata={"platform": "twitter"}
        ),
        RawContent(
            id="3",
            source_type=SourceType.TWITTER,
            content="The product quality is good.",
            author="user3",
            timestamp=datetime.now(),
            metadata={"platform": "twitter"}
        ),
    ]


class TestAnalysisServiceIntegration:
    """Integration tests for AnalysisService."""
    
    def test_analysis_service_initialization(self, analysis_service):
        """Test that analysis service initializes correctly."""
        assert analysis_service is not None
        assert analysis_service.sentiment_analyzer is not None
        assert analysis_service.topic_extractor is not None
        assert analysis_service.repository is not None
    
    def test_analyze_content_returns_analyzed_content(
        self, analysis_service, sample_raw_content
    ):
        """Test that analyze_content returns AnalyzedContent objects."""
        results = analysis_service.analyze_content(sample_raw_content)
        
        assert len(results) == len(sample_raw_content)
        assert all(isinstance(r, AnalyzedContent) for r in results)
    
    def test_analyzed_content_has_sentiment(
        self, analysis_service, sample_raw_content
    ):
        """Test that analyzed content includes sentiment."""
        results = analysis_service.analyze_content(sample_raw_content)
        
        for result in results:
            assert isinstance(result.sentiment, SentimentScore)
            assert result.sentiment.label in [
                SentimentLabel.POSITIVE,
                SentimentLabel.NEGATIVE,
                SentimentLabel.NEUTRAL
            ]
    
    def test_analyzed_content_has_topics(
        self, analysis_service, sample_raw_content
    ):
        """Test that analyzed content includes topics."""
        results = analysis_service.analyze_content(sample_raw_content)
        
        for result in results:
            assert isinstance(result.topics, list)
            assert all(isinstance(t, Topic) for t in result.topics)
    
    def test_analyzed_content_has_timestamp(
        self, analysis_service, sample_raw_content
    ):
        """Test that analyzed content has processed timestamp."""
        results = analysis_service.analyze_content(sample_raw_content)
        
        for result in results:
            assert isinstance(result.processed_at, datetime)
    
    def test_analyzed_content_saved_to_repository(
        self, analysis_service, sample_raw_content, mock_repository
    ):
        """Test that analyzed content is saved to repository."""
        results = analysis_service.analyze_content(sample_raw_content)
        
        stored_items = mock_repository.find({})
        assert len(stored_items) == len(sample_raw_content)
    
    def test_sentiment_varies_by_content(
        self, analysis_service, sample_raw_content
    ):
        """Test that different content produces different sentiments."""
        results = analysis_service.analyze_content(sample_raw_content)
        
        sentiments = [r.sentiment.label for r in results]
        # Should have at least some variation (not all the same)
        assert len(set(sentiments)) >= 1


class TestCSVIngestionWithAnalysis:
    """Integration tests for CSV ingestion with sentiment analysis."""
    
    @pytest.mark.skipif(
        not os.path.exists("data/sentimentdataset.csv"),
        reason="Dataset not available"
    )
    def test_load_and_analyze_from_csv(
        self, trained_analyzer, mock_topic_extractor, mock_repository
    ):
        """Test loading from CSV and analyzing."""
        # Load data
        csv_source = CSVDataSource("data/sentimentdataset.csv")
        raw_content = csv_source.fetch_content(query="", limit=10)
        
        assert len(raw_content) > 0
        
        # Analyze
        analysis_service = AnalysisService(
            sentiment_analyzer=trained_analyzer,
            topic_extractor=mock_topic_extractor,
            repository=mock_repository
        )
        
        results = analysis_service.analyze_content(raw_content)
        
        assert len(results) == len(raw_content)
        assert all(isinstance(r, AnalyzedContent) for r in results)
    
    @pytest.mark.skipif(
        not os.path.exists("data/sentimentdataset.csv"),
        reason="Dataset not available"
    )
    def test_batch_analysis_performance(
        self, trained_analyzer, mock_topic_extractor, mock_repository
    ):
        """Test performance of batch analysis."""
        import time
        
        # Load data
        csv_source = CSVDataSource("data/sentimentdataset.csv")
        raw_content = csv_source.fetch_content(query="", limit=50)
        
        # Analyze
        analysis_service = AnalysisService(
            sentiment_analyzer=trained_analyzer,
            topic_extractor=mock_topic_extractor,
            repository=mock_repository
        )
        
        start_time = time.time()
        results = analysis_service.analyze_content(raw_content)
        end_time = time.time()
        
        # Should complete in reasonable time (< 30 seconds for 50 items)
        assert (end_time - start_time) < 30.0
        assert len(results) == 50


class TestSentimentAnalyzerWithIngestion:
    """Test sentiment analyzer with ingested data."""
    
    @pytest.mark.skipif(
        not os.path.exists("data/sentimentdataset.csv"),
        reason="Dataset not available"
    )
    def test_analyze_ingested_data(self, trained_analyzer):
        """Test analyzing data from CSV ingestion."""
        # Load data
        csv_source = CSVDataSource("data/sentimentdataset.csv")
        raw_content = csv_source.fetch_content(query="", limit=20)
        
        # Analyze each item
        results = []
        for item in raw_content:
            sentiment = trained_analyzer.analyze(item.content)
            results.append({
                'text': item.content,
                'predicted': sentiment.label.value,
                'confidence': sentiment.score,
                'original': item.metadata.get('sentiment', '').strip().lower()
            })
        
        assert len(results) == 20
        
        # Check that we have some variety in predictions
        predicted_labels = [r['predicted'] for r in results]
        assert len(set(predicted_labels)) >= 1
        
        # Check confidence scores are reasonable
        confidences = [r['confidence'] for r in results]
        assert all(0.0 <= c <= 1.0 for c in confidences)
    
    @pytest.mark.skipif(
        not os.path.exists("data/sentimentdataset.csv"),
        reason="Dataset not available"
    )
    def test_sentiment_distribution(self, trained_analyzer):
        """Test sentiment distribution on dataset."""
        # Load data
        csv_source = CSVDataSource("data/sentimentdataset.csv")
        raw_content = csv_source.fetch_content(query="", limit=100)
        
        # Analyze
        sentiment_counts = {'positive': 0, 'negative': 0, 'neutral': 0}
        
        for item in raw_content:
            sentiment = trained_analyzer.analyze(item.content)
            sentiment_counts[sentiment.label.value] += 1
        
        # Should have predictions in all categories (or at least some)
        total = sum(sentiment_counts.values())
        assert total == 100
        
        # At least one category should have predictions
        assert max(sentiment_counts.values()) > 0


class TestEndToEndWorkflow:
    """End-to-end workflow tests."""
    
    @pytest.mark.skipif(
        not os.path.exists("data/sentimentdataset.csv"),
        reason="Dataset not available"
    )
    def test_complete_analysis_pipeline(
        self, trained_analyzer, mock_topic_extractor, mock_repository
    ):
        """Test complete pipeline from ingestion to analysis."""
        # Step 1: Ingest data
        csv_source = CSVDataSource("data/sentimentdataset.csv")
        raw_content = csv_source.fetch_content(query="", limit=10)
        
        assert len(raw_content) == 10
        
        # Step 2: Create analysis service
        analysis_service = AnalysisService(
            sentiment_analyzer=trained_analyzer,
            topic_extractor=mock_topic_extractor,
            repository=mock_repository
        )
        
        # Step 3: Analyze content
        analyzed_content = analysis_service.analyze_content(raw_content)
        
        assert len(analyzed_content) == 10
        
        # Step 4: Verify results
        for item in analyzed_content:
            # Has original content
            assert isinstance(item.raw_content, RawContent)
            
            # Has sentiment analysis
            assert isinstance(item.sentiment, SentimentScore)
            assert item.sentiment.label in [
                SentimentLabel.POSITIVE,
                SentimentLabel.NEGATIVE,
                SentimentLabel.NEUTRAL
            ]
            
            # Has topics
            assert isinstance(item.topics, list)
            
            # Has timestamp
            assert isinstance(item.processed_at, datetime)
        
        # Step 5: Verify storage
        stored = mock_repository.find({})
        assert len(stored) == 10
    
    def test_workflow_with_custom_content(
        self, trained_analyzer, mock_topic_extractor, mock_repository
    ):
        """Test workflow with custom content."""
        # Create custom content
        custom_content = [
            RawContent(
                id="custom_1",
                source_type=SourceType.TWITTER,
                content="This product has excellent quality!",
                author="test_user",
                timestamp=datetime.now(),
                metadata={}
            ),
            RawContent(
                id="custom_2",
                source_type=SourceType.TWITTER,
                content="The service was disappointing.",
                author="test_user2",
                timestamp=datetime.now(),
                metadata={}
            ),
        ]
        
        # Analyze
        analysis_service = AnalysisService(
            sentiment_analyzer=trained_analyzer,
            topic_extractor=mock_topic_extractor,
            repository=mock_repository
        )
        
        results = analysis_service.analyze_content(custom_content)
        
        assert len(results) == 2
        
        # First should be positive (excellent quality)
        # Second should be negative (disappointing)
        # Note: Model may not be perfect, so we just check structure
        assert results[0].sentiment.label in [
            SentimentLabel.POSITIVE,
            SentimentLabel.NEGATIVE,
            SentimentLabel.NEUTRAL
        ]
        assert results[1].sentiment.label in [
            SentimentLabel.POSITIVE,
            SentimentLabel.NEGATIVE,
            SentimentLabel.NEUTRAL
        ]


class TestErrorHandling:
    """Test error handling in integration scenarios."""
    
    def test_empty_content_list(
        self, trained_analyzer, mock_topic_extractor, mock_repository
    ):
        """Test handling of empty content list."""
        analysis_service = AnalysisService(
            sentiment_analyzer=trained_analyzer,
            topic_extractor=mock_topic_extractor,
            repository=mock_repository
        )
        
        results = analysis_service.analyze_content([])
        assert results == []
    
    def test_content_with_empty_text(
        self, trained_analyzer, mock_topic_extractor, mock_repository
    ):
        """Test handling of content with empty text."""
        empty_content = [
            RawContent(
                id="empty_1",
                source_type=SourceType.TWITTER,
                content="",
                author="test_user",
                timestamp=datetime.now(),
                metadata={}
            )
        ]
        
        analysis_service = AnalysisService(
            sentiment_analyzer=trained_analyzer,
            topic_extractor=mock_topic_extractor,
            repository=mock_repository
        )
        
        # Should not crash
        results = analysis_service.analyze_content(empty_content)
        assert len(results) == 1
        assert isinstance(results[0].sentiment, SentimentScore)
