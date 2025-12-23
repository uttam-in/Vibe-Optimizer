"""
Unit tests for CSV ingestion service.
Tests CSVDataSource and IngestionService with CSV data.
"""
import pytest
import os
import tempfile
from datetime import datetime
from unittest.mock import Mock, MagicMock

from src.ingestion.ingestion_service import CSVDataSource, IngestionService
from src.core.models import RawContent, SourceType
from src.core.interfaces import IRepository


# Sample CSV data for testing
SAMPLE_CSV_DATA = """,Unnamed: 0,Text,Sentiment,Timestamp,User,Platform,Hashtags,Retweets,Likes,Country,Year,Month,Day,Hour
0,0, Enjoying a beautiful day at the park!              , Positive  ,2023-01-15 12:30:00, User123      , Twitter  , #Nature #Park                            ,15.0,30.0, USA      ,2023,1,15,12
1,1, Traffic was terrible this morning.                 , Negative  ,2023-01-15 08:45:00, CommuterX    , Twitter  , #Traffic #Morning                        ,5.0,10.0, Canada   ,2023,1,15,8
2,2, Just finished an amazing workout! 💪               , Positive  ,2023-01-15 15:45:00, FitnessFan   , Instagram , #Fitness #Workout                        ,20.0,40.0, USA        ,2023,1,15,15
3,3, Excited about the upcoming weekend getaway!        , Positive  ,2023-01-15 18:20:00, AdventureX   , Facebook , #Travel #Adventure                       ,8.0,15.0, UK       ,2023,1,15,18
4,4, Trying out a new recipe for dinner tonight.        , Neutral   ,2023-01-15 19:55:00, ChefCook     , Instagram , #Cooking #Food                           ,12.0,25.0, Australia ,2023,1,15,19
"""


@pytest.fixture
def temp_csv_file():
    """Create a temporary CSV file for testing."""
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv', encoding='utf-8') as f:
        f.write(SAMPLE_CSV_DATA)
        temp_path = f.name
    
    yield temp_path
    
    # Cleanup
    if os.path.exists(temp_path):
        os.remove(temp_path)


@pytest.fixture
def mock_repository():
    """Create a mock repository."""
    repo = Mock(spec=IRepository)
    repo.save = MagicMock(return_value="mock_id")
    return repo


class TestCSVDataSource:
    """Test suite for CSVDataSource class."""
    
    def test_init_with_valid_file(self, temp_csv_file):
        """Test initialization with a valid CSV file."""
        source = CSVDataSource(temp_csv_file)
        assert source.csv_path == temp_csv_file
        assert source.source_type == SourceType.TWITTER
    
    def test_init_with_custom_source_type(self, temp_csv_file):
        """Test initialization with custom source type."""
        source = CSVDataSource(temp_csv_file, SourceType.REDDIT)
        assert source.source_type == SourceType.REDDIT
    
    def test_init_with_nonexistent_file(self):
        """Test initialization with nonexistent file raises error."""
        with pytest.raises(FileNotFoundError):
            CSVDataSource("nonexistent_file.csv")
    
    def test_fetch_content_all(self, temp_csv_file):
        """Test fetching all content from CSV."""
        source = CSVDataSource(temp_csv_file)
        content = source.fetch_content()
        
        assert len(content) == 5
        assert all(isinstance(item, RawContent) for item in content)
    
    def test_fetch_content_with_limit(self, temp_csv_file):
        """Test fetching content with limit."""
        source = CSVDataSource(temp_csv_file)
        content = source.fetch_content(limit=3)
        
        assert len(content) == 3
    
    def test_fetch_content_with_query(self, temp_csv_file):
        """Test fetching content with text query filter."""
        source = CSVDataSource(temp_csv_file)
        content = source.fetch_content(query="workout")
        
        assert len(content) == 1
        assert "workout" in content[0].content.lower()
    
    def test_fetch_content_with_since_date(self, temp_csv_file):
        """Test fetching content since a specific date."""
        source = CSVDataSource(temp_csv_file)
        since_date = datetime(2023, 1, 15, 16, 0, 0)
        content = source.fetch_content(since=since_date)
        
        # Should get 2 items (18:20 and 19:55)
        assert len(content) == 2
        assert all(item.timestamp >= since_date for item in content)
    
    def test_fetch_content_query_case_insensitive(self, temp_csv_file):
        """Test query filtering is case insensitive."""
        source = CSVDataSource(temp_csv_file)
        content_lower = source.fetch_content(query="traffic")
        content_upper = source.fetch_content(query="TRAFFIC")
        
        assert len(content_lower) == len(content_upper) == 1
    
    def test_raw_content_structure(self, temp_csv_file):
        """Test that RawContent objects have correct structure."""
        source = CSVDataSource(temp_csv_file)
        content = source.fetch_content(limit=1)
        
        item = content[0]
        assert item.id == "0"
        assert item.content == "Enjoying a beautiful day at the park!"
        assert item.author == "User123"
        assert item.timestamp == datetime(2023, 1, 15, 12, 30, 0)
        assert item.source_type == SourceType.TWITTER
        assert item.metadata['sentiment'] == "Positive"
        assert item.metadata['platform'] == "twitter"
        assert item.metadata['hashtags'] == "#Nature #Park"
        assert item.metadata['retweets'] == 15.0
        assert item.metadata['likes'] == 30.0
        assert item.metadata['country'] == "USA"
    
    def test_platform_mapping(self, temp_csv_file):
        """Test platform to SourceType mapping."""
        source = CSVDataSource(temp_csv_file)
        content = source.fetch_content()
        
        # Check different platforms are mapped
        platforms = [item.metadata['platform'] for item in content]
        assert 'twitter' in platforms
        assert 'instagram' in platforms
        assert 'facebook' in platforms
    
    def test_get_source_type(self, temp_csv_file):
        """Test get_source_type method."""
        source = CSVDataSource(temp_csv_file, SourceType.REDDIT)
        assert source.get_source_type() == SourceType.REDDIT
    
    def test_safe_float_conversion(self, temp_csv_file):
        """Test safe float conversion in metadata."""
        source = CSVDataSource(temp_csv_file)
        content = source.fetch_content(limit=1)
        
        item = content[0]
        assert isinstance(item.metadata['retweets'], float)
        assert isinstance(item.metadata['likes'], float)
    
    def test_empty_query_returns_all(self, temp_csv_file):
        """Test that empty query returns all content."""
        source = CSVDataSource(temp_csv_file)
        content_all = source.fetch_content()
        content_empty_query = source.fetch_content(query="")
        
        assert len(content_all) == len(content_empty_query)


class TestIngestionService:
    """Test suite for IngestionService class."""
    
    def test_init(self, mock_repository):
        """Test IngestionService initialization."""
        sources = []
        service = IngestionService(sources, mock_repository)
        
        assert service.sources == sources
        assert service.repository == mock_repository
    
    def test_ingest_all_with_single_source(self, temp_csv_file, mock_repository):
        """Test ingesting from a single source."""
        csv_source = CSVDataSource(temp_csv_file)
        service = IngestionService([csv_source], mock_repository)
        
        content = service.ingest_all(limit_per_source=10)
        
        assert len(content) == 5
        assert mock_repository.save.call_count == 5
    
    def test_ingest_all_with_multiple_sources(self, temp_csv_file, mock_repository):
        """Test ingesting from multiple sources."""
        csv_source1 = CSVDataSource(temp_csv_file)
        csv_source2 = CSVDataSource(temp_csv_file)
        service = IngestionService([csv_source1, csv_source2], mock_repository)
        
        content = service.ingest_all(limit_per_source=10)
        
        # Should get 10 items (5 from each source)
        assert len(content) == 10
        assert mock_repository.save.call_count == 10
    
    def test_ingest_all_with_query(self, temp_csv_file, mock_repository):
        """Test ingesting with query filter."""
        csv_source = CSVDataSource(temp_csv_file)
        service = IngestionService([csv_source], mock_repository)
        
        content = service.ingest_all(query="park")
        
        assert len(content) == 1
        assert "park" in content[0].content.lower()
    
    def test_ingest_all_with_since_date(self, temp_csv_file, mock_repository):
        """Test ingesting with since date filter."""
        csv_source = CSVDataSource(temp_csv_file)
        service = IngestionService([csv_source], mock_repository)
        
        since_date = datetime(2023, 1, 15, 16, 0, 0)
        content = service.ingest_all(since=since_date)
        
        assert len(content) == 2
        assert all(item.timestamp >= since_date for item in content)
    
    def test_ingest_all_error_handling(self, mock_repository, capsys):
        """Test error handling when source fails."""
        # Create a mock source that raises an exception
        failing_source = Mock(spec=CSVDataSource)
        failing_source.fetch_content.side_effect = Exception("Test error")
        failing_source.get_source_type.return_value = SourceType.TWITTER
        
        service = IngestionService([failing_source], mock_repository)
        content = service.ingest_all()
        
        # Should return empty list and print error
        assert len(content) == 0
        captured = capsys.readouterr()
        assert "Error ingesting" in captured.out
    
    def test_ingest_from_csv_convenience_method(self, temp_csv_file, mock_repository):
        """Test ingest_from_csv convenience method."""
        service = IngestionService([], mock_repository)
        content = service.ingest_from_csv(temp_csv_file, limit=3)
        
        assert len(content) == 3
        assert mock_repository.save.call_count == 3
    
    def test_ingest_from_csv_with_query(self, temp_csv_file, mock_repository):
        """Test ingest_from_csv with query filter."""
        service = IngestionService([], mock_repository)
        content = service.ingest_from_csv(temp_csv_file, query="workout")
        
        assert len(content) == 1
        assert "workout" in content[0].content.lower()
    
    def test_add_source(self, temp_csv_file, mock_repository):
        """Test adding a source dynamically."""
        service = IngestionService([], mock_repository)
        assert len(service.sources) == 0
        
        csv_source = CSVDataSource(temp_csv_file)
        service.add_source(csv_source)
        
        assert len(service.sources) == 1
        assert service.sources[0] == csv_source
    
    def test_remove_source(self, temp_csv_file, mock_repository):
        """Test removing a source."""
        csv_source = CSVDataSource(temp_csv_file, SourceType.TWITTER)
        service = IngestionService([csv_source], mock_repository)
        
        assert len(service.sources) == 1
        
        service.remove_source("twitter")
        
        assert len(service.sources) == 0
    
    def test_remove_source_keeps_others(self, temp_csv_file, mock_repository):
        """Test removing a source keeps other sources."""
        twitter_source = CSVDataSource(temp_csv_file, SourceType.TWITTER)
        reddit_source = CSVDataSource(temp_csv_file, SourceType.REDDIT)
        service = IngestionService([twitter_source, reddit_source], mock_repository)
        
        service.remove_source("twitter")
        
        assert len(service.sources) == 1
        assert service.sources[0].get_source_type() == SourceType.REDDIT


class TestIntegration:
    """Integration tests using actual dataset."""
    
    def test_ingest_from_actual_dataset(self, mock_repository):
        """Test ingesting from the actual sentiment dataset."""
        dataset_path = "data/sentimentdataset.csv"
        
        # Skip if dataset doesn't exist
        if not os.path.exists(dataset_path):
            pytest.skip("Dataset file not found")
        
        csv_source = CSVDataSource(dataset_path)
        service = IngestionService([csv_source], mock_repository)
        
        # Ingest first 10 items
        content = service.ingest_all(limit_per_source=10)
        
        assert len(content) == 10
        assert all(isinstance(item, RawContent) for item in content)
        assert mock_repository.save.call_count == 10
    
    def test_ingest_positive_sentiment(self, mock_repository):
        """Test filtering positive sentiment from actual dataset."""
        dataset_path = "data/sentimentdataset.csv"
        
        if not os.path.exists(dataset_path):
            pytest.skip("Dataset file not found")
        
        csv_source = CSVDataSource(dataset_path)
        content = csv_source.fetch_content(limit=50)
        
        # Filter positive sentiments
        positive_content = [
            item for item in content 
            if 'positive' in item.metadata.get('sentiment', '').lower()
        ]
        
        assert len(positive_content) > 0
    
    def test_ingest_by_date_range(self, mock_repository):
        """Test ingesting content within a date range."""
        dataset_path = "data/sentimentdataset.csv"
        
        if not os.path.exists(dataset_path):
            pytest.skip("Dataset file not found")
        
        csv_source = CSVDataSource(dataset_path)
        since_date = datetime(2023, 1, 15, 0, 0, 0)
        content = csv_source.fetch_content(since=since_date, limit=100)
        
        assert all(item.timestamp >= since_date for item in content)
