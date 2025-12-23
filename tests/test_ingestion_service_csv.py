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
    
    def test_fetch_with_zero_limit(self, temp_csv_file):
        """Test fetching content with zero limit returns empty list."""
        source = CSVDataSource(temp_csv_file)
        content = source.fetch_content(limit=0)
        
        assert len(content) == 0
    
    def test_fetch_with_large_limit(self, temp_csv_file):
        """Test fetching with limit larger than available data."""
        source = CSVDataSource(temp_csv_file)
        content = source.fetch_content(limit=1000)
        
        # Should return all 5 items, not 1000
        assert len(content) == 5
    
    def test_combined_query_and_since_filter(self, temp_csv_file):
        """Test using both query and since filters together."""
        source = CSVDataSource(temp_csv_file)
        since_date = datetime(2023, 1, 15, 10, 0, 0)
        content = source.fetch_content(query="positive", since=since_date)
        
        # Should filter by both conditions
        assert all(item.timestamp >= since_date for item in content)
        assert all("positive" in item.metadata.get('sentiment', '').lower() for item in content)
    
    def test_query_with_special_characters(self, temp_csv_file):
        """Test query with special characters like emoji."""
        source = CSVDataSource(temp_csv_file)
        content = source.fetch_content(query="💪")
        
        assert len(content) == 1
        assert "💪" in content[0].content
    
    def test_metadata_with_missing_values(self):
        """Test handling CSV with missing metadata values."""
        csv_data = """,Unnamed: 0,Text,Sentiment,Timestamp,User,Platform,Hashtags,Retweets,Likes,Country
0,0,Test content,Positive,2023-01-15 12:30:00,User1,Twitter,,,,,
"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv', encoding='utf-8') as f:
            f.write(csv_data)
            temp_path = f.name
        
        try:
            source = CSVDataSource(temp_path)
            content = source.fetch_content()
            
            assert len(content) == 1
            assert content[0].metadata['retweets'] is None
            assert content[0].metadata['likes'] is None
            assert content[0].metadata['country'] == ""
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)
    
    def test_invalid_timestamp_skipped(self):
        """Test that rows with invalid timestamps are skipped."""
        csv_data = """,Unnamed: 0,Text,Sentiment,Timestamp,User,Platform
0,0,Valid content,Positive,2023-01-15 12:30:00,User1,Twitter
1,1,Invalid timestamp,Positive,invalid-date,User2,Twitter
2,2,Another valid,Positive,2023-01-15 13:30:00,User3,Twitter
"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv', encoding='utf-8') as f:
            f.write(csv_data)
            temp_path = f.name
        
        try:
            source = CSVDataSource(temp_path)
            content = source.fetch_content()
            
            # Should skip the row with invalid timestamp
            assert len(content) == 2
            assert all(isinstance(item.timestamp, datetime) for item in content)
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)
    
    def test_empty_csv_file(self):
        """Test handling of empty CSV file."""
        csv_data = """,Unnamed: 0,Text,Sentiment,Timestamp,User,Platform
"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv', encoding='utf-8') as f:
            f.write(csv_data)
            temp_path = f.name
        
        try:
            source = CSVDataSource(temp_path)
            content = source.fetch_content()
            
            assert len(content) == 0
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)
    
    def test_unknown_platform_mapping(self):
        """Test that unknown platforms default to TWITTER."""
        csv_data = """,Unnamed: 0,Text,Sentiment,Timestamp,User,Platform
0,0,Test content,Positive,2023-01-15 12:30:00,User1,UnknownPlatform
"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv', encoding='utf-8') as f:
            f.write(csv_data)
            temp_path = f.name
        
        try:
            source = CSVDataSource(temp_path)
            content = source.fetch_content()
            
            assert len(content) == 1
            assert content[0].source_type == SourceType.TWITTER
            assert content[0].metadata['platform'] == 'unknownplatform'
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)
    
    def test_whitespace_handling(self, temp_csv_file):
        """Test that whitespace is properly stripped from fields."""
        source = CSVDataSource(temp_csv_file)
        content = source.fetch_content(limit=1)
        
        # Check that content doesn't have leading/trailing whitespace
        assert content[0].content == "Enjoying a beautiful day at the park!"
        assert content[0].author == "User123"
        assert content[0].metadata['sentiment'] == "Positive"
    
    def test_fetch_content_respects_exact_limit(self, temp_csv_file):
        """Test that fetch_content returns exactly the limit when available."""
        source = CSVDataSource(temp_csv_file)
        
        for limit in [1, 2, 3, 4, 5]:
            content = source.fetch_content(limit=limit)
            assert len(content) == limit
    
    def test_safe_float_with_invalid_values(self):
        """Test safe float conversion with various invalid inputs."""
        csv_data = """,Unnamed: 0,Text,Sentiment,Timestamp,User,Platform,Retweets,Likes
0,0,Test,Positive,2023-01-15 12:30:00,User1,Twitter,abc,xyz
1,1,Test2,Positive,2023-01-15 12:30:00,User2,Twitter,10.5,20.5
"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv', encoding='utf-8') as f:
            f.write(csv_data)
            temp_path = f.name
        
        try:
            source = CSVDataSource(temp_path)
            content = source.fetch_content()
            
            assert len(content) == 2
            # First row should have None for invalid floats
            assert content[0].metadata['retweets'] is None
            assert content[0].metadata['likes'] is None
            # Second row should have valid floats
            assert content[1].metadata['retweets'] == 10.5
            assert content[1].metadata['likes'] == 20.5
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)
    
    def test_author_field_handling(self):
        """Test handling of missing or empty author fields."""
        csv_data = """,Unnamed: 0,Text,Sentiment,Timestamp,User,Platform
0,0,Test with author,Positive,2023-01-15 12:30:00,ValidUser,Twitter
1,1,Test without author,Positive,2023-01-15 12:30:00,,Twitter
"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv', encoding='utf-8') as f:
            f.write(csv_data)
            temp_path = f.name
        
        try:
            source = CSVDataSource(temp_path)
            content = source.fetch_content()
            
            assert len(content) == 2
            assert content[0].author == "ValidUser"
            assert content[1].author is None
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)
    
    def test_query_no_matches(self, temp_csv_file):
        """Test query that matches no content."""
        source = CSVDataSource(temp_csv_file)
        content = source.fetch_content(query="nonexistentquery12345")
        
        assert len(content) == 0
    
    def test_since_date_future(self, temp_csv_file):
        """Test since date in the future returns no content."""
        source = CSVDataSource(temp_csv_file)
        future_date = datetime(2025, 1, 1, 0, 0, 0)
        content = source.fetch_content(since=future_date)
        
        assert len(content) == 0
    
    def test_multiple_hashtags_preserved(self, temp_csv_file):
        """Test that multiple hashtags are preserved correctly."""
        source = CSVDataSource(temp_csv_file)
        content = source.fetch_content(limit=1)
        
        assert content[0].metadata['hashtags'] == "#Nature #Park"


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
    
    def test_ingest_all_with_empty_sources(self, mock_repository):
        """Test ingesting with no sources configured."""
        service = IngestionService([], mock_repository)
        content = service.ingest_all()
        
        assert len(content) == 0
        assert mock_repository.save.call_count == 0
    
    def test_ingest_all_respects_limit_per_source(self, temp_csv_file, mock_repository):
        """Test that limit_per_source is respected for each source."""
        csv_source = CSVDataSource(temp_csv_file)
        service = IngestionService([csv_source], mock_repository)
        
        content = service.ingest_all(limit_per_source=2)
        
        assert len(content) == 2
        assert mock_repository.save.call_count == 2
    
    def test_ingest_all_combines_filters(self, temp_csv_file, mock_repository):
        """Test ingesting with both query and since filters."""
        csv_source = CSVDataSource(temp_csv_file)
        service = IngestionService([csv_source], mock_repository)
        
        since_date = datetime(2023, 1, 15, 15, 0, 0)
        content = service.ingest_all(query="positive", since=since_date)
        
        # Should have items that match both filters
        assert all(item.timestamp >= since_date for item in content)
        assert all("positive" in item.metadata.get('sentiment', '').lower() for item in content)
    
    def test_repository_save_called_with_correct_data(self, temp_csv_file, mock_repository):
        """Test that repository.save is called with RawContent objects."""
        csv_source = CSVDataSource(temp_csv_file)
        service = IngestionService([csv_source], mock_repository)
        
        content = service.ingest_all(limit_per_source=1)
        
        # Verify save was called with RawContent
        assert mock_repository.save.call_count == 1
        saved_item = mock_repository.save.call_args[0][0]
        assert isinstance(saved_item, RawContent)
        assert saved_item.content == "Enjoying a beautiful day at the park!"
    
    def test_ingest_from_csv_with_since_filter(self, temp_csv_file, mock_repository):
        """Test ingest_from_csv with since date filter."""
        service = IngestionService([], mock_repository)
        since_date = datetime(2023, 1, 15, 18, 0, 0)
        content = service.ingest_from_csv(temp_csv_file, since=since_date)
        
        assert len(content) == 2
        assert all(item.timestamp >= since_date for item in content)
    
    def test_ingest_from_csv_with_combined_filters(self, temp_csv_file, mock_repository):
        """Test ingest_from_csv with query and since filters combined."""
        service = IngestionService([], mock_repository)
        since_date = datetime(2023, 1, 15, 10, 0, 0)
        content = service.ingest_from_csv(
            temp_csv_file, 
            query="positive", 
            since=since_date,
            limit=10
        )
        
        assert all(item.timestamp >= since_date for item in content)
        assert all("positive" in item.metadata.get('sentiment', '').lower() for item in content)
    
    def test_add_multiple_sources(self, temp_csv_file, mock_repository):
        """Test adding multiple sources dynamically."""
        service = IngestionService([], mock_repository)
        
        source1 = CSVDataSource(temp_csv_file, SourceType.TWITTER)
        source2 = CSVDataSource(temp_csv_file, SourceType.REDDIT)
        
        service.add_source(source1)
        service.add_source(source2)
        
        assert len(service.sources) == 2
        assert service.sources[0].get_source_type() == SourceType.TWITTER
        assert service.sources[1].get_source_type() == SourceType.REDDIT
    
    def test_remove_nonexistent_source(self, temp_csv_file, mock_repository):
        """Test removing a source that doesn't exist."""
        csv_source = CSVDataSource(temp_csv_file, SourceType.TWITTER)
        service = IngestionService([csv_source], mock_repository)
        
        # Try to remove a source type that doesn't exist
        service.remove_source("reddit")
        
        # Original source should still be there
        assert len(service.sources) == 1
        assert service.sources[0].get_source_type() == SourceType.TWITTER
    
    def test_ingest_all_partial_failure(self, temp_csv_file, mock_repository, capsys):
        """Test that ingestion continues when one source fails."""
        # Create one valid and one failing source
        valid_source = CSVDataSource(temp_csv_file)
        failing_source = Mock(spec=CSVDataSource)
        failing_source.fetch_content.side_effect = Exception("Source failed")
        failing_source.get_source_type.return_value = SourceType.REDDIT
        
        service = IngestionService([failing_source, valid_source], mock_repository)
        content = service.ingest_all(limit_per_source=10)
        
        # Should get content from valid source despite failure
        assert len(content) == 5
        assert mock_repository.save.call_count == 5
        
        # Should print error message
        captured = capsys.readouterr()
        assert "Error ingesting" in captured.out
    
    def test_ingest_all_with_zero_limit(self, temp_csv_file, mock_repository):
        """Test ingesting with zero limit per source."""
        csv_source = CSVDataSource(temp_csv_file)
        service = IngestionService([csv_source], mock_repository)
        
        content = service.ingest_all(limit_per_source=0)
        
        assert len(content) == 0
        assert mock_repository.save.call_count == 0
    
    def test_ingest_from_csv_nonexistent_file(self, mock_repository):
        """Test ingest_from_csv with nonexistent file raises error."""
        service = IngestionService([], mock_repository)
        
        with pytest.raises(FileNotFoundError):
            service.ingest_from_csv("nonexistent_file.csv")


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
