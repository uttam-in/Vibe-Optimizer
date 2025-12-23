# Ingestion Service Testing Documentation

## Overview

This document describes the test suite for the Ingestion Service, covering unit tests, integration tests, and testing strategies.

## Test Structure

The test suite is organized into three main classes:

1. **TestCSVDataSource** - Unit tests for CSV data source
2. **TestIngestionService** - Unit tests for the orchestration service
3. **TestIntegration** - Integration tests with real datasets

## Test Fixtures

### temp_csv_file

Creates a temporary CSV file with sample social media data for testing.

**Data includes:**
- 5 sample posts from different platforms (Twitter, Instagram, Facebook)
- Various sentiments (Positive, Negative, Neutral)
- Different timestamps on 2023-01-15
- Metadata: hashtags, likes, retweets, countries

**Lifecycle:**
- Created before each test that uses it
- Automatically deleted after test completion

### mock_repository

Creates a mock `IRepository` object for testing without database dependencies.

**Behavior:**
- `save()` method returns "mock_id"
- Tracks call count for verification
- No actual data persistence

## Test Cases

### TestCSVDataSource (13 tests)

#### Initialization Tests

**test_init_with_valid_file**
- Verifies CSV source initializes with valid file path
- Confirms default source type is `SourceType.TWITTER`
- Ensures file path is stored correctly

**test_init_with_custom_source_type**
- Tests initialization with custom source type (Reddit)
- Validates source type override works

**test_init_with_nonexistent_file**
- Ensures `FileNotFoundError` is raised for missing files
- Tests error handling at initialization

#### Content Fetching Tests

**test_fetch_content_all**
- Fetches all 5 rows from sample CSV
- Validates all items are `RawContent` objects
- Confirms no data loss during parsing

**test_fetch_content_with_limit**
- Tests limit parameter (limit=3 returns 3 items)
- Validates pagination/limiting functionality

**test_fetch_content_with_query**
- Tests text filtering with query="workout"
- Confirms case-insensitive search
- Validates only matching content is returned

**test_fetch_content_with_since_date**
- Filters content after 4 PM (16:00)
- Expects 2 items (18:20 and 19:55 timestamps)
- Validates date comparison logic

**test_fetch_content_query_case_insensitive**
- Tests "traffic" vs "TRAFFIC" queries
- Confirms both return identical results
- Validates case-insensitive implementation

**test_empty_query_returns_all**
- Empty query string returns all content
- Validates default behavior

#### Data Structure Tests

**test_raw_content_structure**
- Validates complete `RawContent` object structure
- Checks all fields: id, content, author, timestamp, source_type
- Verifies metadata dictionary contents
- Confirms data type conversions

**test_platform_mapping**
- Tests platform string to `SourceType` mapping
- Validates Twitter, Instagram, Facebook platforms are recognized
- Ensures correct enum assignment

**test_safe_float_conversion**
- Tests numeric field conversion (retweets, likes)
- Validates float type for numeric metadata
- Ensures safe handling of malformed numbers

**test_get_source_type**
- Tests getter method returns correct source type
- Validates method contract

### TestIngestionService (11 tests)

#### Initialization Tests

**test_init**
- Validates service initialization with sources and repository
- Confirms attributes are set correctly

#### Ingestion Tests

**test_ingest_all_with_single_source**
- Ingests from one CSV source
- Expects 5 items returned
- Validates repository.save() called 5 times

**test_ingest_all_with_multiple_sources**
- Uses 2 identical CSV sources
- Expects 10 total items (5 from each)
- Validates repository.save() called 10 times
- Tests multi-source aggregation

**test_ingest_all_with_query**
- Tests query filtering through service layer
- Query="park" returns 1 matching item
- Validates filter propagation to sources

**test_ingest_all_with_since_date**
- Tests date filtering through service
- Since date at 16:00 returns 2 items
- Validates timestamp filtering

**test_ingest_all_error_handling**
- Creates mock source that raises exception
- Service continues execution (doesn't crash)
- Returns empty list
- Prints error message to stdout
- Tests resilience and error recovery

#### Convenience Method Tests

**test_ingest_from_csv_convenience_method**
- Tests shortcut method for CSV ingestion
- Creates CSV source internally
- Limit=3 returns 3 items
- Validates repository saves

**test_ingest_from_csv_with_query**
- Tests convenience method with query filter
- Query="workout" returns 1 item
- Validates filtering works in convenience method

#### Dynamic Source Management Tests

**test_add_source**
- Starts with empty sources list
- Adds one source dynamically
- Validates source is added to list

**test_remove_source**
- Starts with one Twitter source
- Removes by source type "twitter"
- Validates sources list is empty

**test_remove_source_keeps_others**
- Starts with Twitter and Reddit sources
- Removes only Twitter
- Validates Reddit source remains
- Tests selective removal

### TestIntegration (3 tests)

These tests use the actual `data/sentimentdataset.csv` file and are skipped if the file doesn't exist.

**test_ingest_from_actual_dataset**
- Ingests first 10 items from real dataset
- Validates all are `RawContent` objects
- Confirms repository saves work
- Tests real-world data compatibility

**test_ingest_positive_sentiment**
- Fetches 50 items from real dataset
- Filters for positive sentiment
- Validates sentiment metadata exists
- Tests sentiment-based filtering

**test_ingest_by_date_range**
- Fetches content since 2023-01-15
- Validates all timestamps are after filter date
- Tests date range queries on real data

## Running Tests

### Run All Tests

```bash
pytest tests/test_ingestion_service_csv.py -v
```

### Run Specific Test Class

```bash
# CSV Data Source tests only
pytest tests/test_ingestion_service_csv.py::TestCSVDataSource -v

# Ingestion Service tests only
pytest tests/test_ingestion_service_csv.py::TestIngestionService -v

# Integration tests only
pytest tests/test_ingestion_service_csv.py::TestIntegration -v
```

### Run Specific Test

```bash
pytest tests/test_ingestion_service_csv.py::TestCSVDataSource::test_fetch_content_with_query -v
```

### Run with Coverage

```bash
pytest tests/test_ingestion_service_csv.py --cov=src.ingestion --cov-report=html
```

### Run with Output Capture

```bash
# See print statements
pytest tests/test_ingestion_service_csv.py -v -s
```

## Test Coverage

Current coverage areas:

✅ **Covered:**
- CSV file reading and parsing
- Data filtering (query, date, limit)
- Error handling (missing files, invalid data)
- Multi-source ingestion
- Repository integration
- Dynamic source management
- Platform mapping
- Data type conversions
- Case-insensitive search

❌ **Not Covered:**
- Network-based data sources (API calls)
- Large file performance
- Concurrent ingestion
- Database repository (only mock tested)
- CSV encoding issues
- Malformed CSV structure

## Testing Best Practices

### Isolation

Each test is independent:
- Uses temporary files (auto-cleanup)
- Uses mock repositories (no side effects)
- No shared state between tests

### Clarity

Tests follow naming convention:
- `test_<method>_<scenario>` format
- Descriptive names explain what's being tested
- One assertion per logical concept

### Fixtures

Reusable test data:
- `temp_csv_file` for consistent test data
- `mock_repository` for dependency injection
- Automatic cleanup prevents pollution

### Assertions

Clear validation:
- Check return values
- Verify call counts
- Validate data structure
- Test edge cases

## Common Testing Patterns

### Testing with Filters

```python
def test_with_filters(temp_csv_file, mock_repository):
    source = CSVDataSource(temp_csv_file)
    content = source.fetch_content(
        query="keyword",
        since=datetime(2023, 1, 15, 12, 0, 0),
        limit=10
    )
    assert len(content) <= 10
    assert all("keyword" in item.content.lower() for item in content)
```

### Testing Error Handling

```python
def test_error_handling(mock_repository, capsys):
    failing_source = Mock(spec=CSVDataSource)
    failing_source.fetch_content.side_effect = Exception("Error")
    
    service = IngestionService([failing_source], mock_repository)
    content = service.ingest_all()
    
    assert len(content) == 0
    captured = capsys.readouterr()
    assert "Error" in captured.out
```

### Testing Repository Integration

```python
def test_repository_saves(temp_csv_file, mock_repository):
    service = IngestionService([CSVDataSource(temp_csv_file)], mock_repository)
    content = service.ingest_all()
    
    assert mock_repository.save.call_count == len(content)
```

## Debugging Failed Tests

### Check Temporary File

```python
@pytest.fixture
def temp_csv_file():
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
        f.write(SAMPLE_CSV_DATA)
        temp_path = f.name
        print(f"Created temp file: {temp_path}")  # Debug output
    yield temp_path
    os.remove(temp_path)
```

### Inspect Test Data

```python
def test_debug_content(temp_csv_file):
    source = CSVDataSource(temp_csv_file)
    content = source.fetch_content()
    
    for item in content:
        print(f"ID: {item.id}, Content: {item.content[:50]}")
    
    assert len(content) > 0
```

### Verify Mock Calls

```python
def test_mock_verification(temp_csv_file, mock_repository):
    service = IngestionService([CSVDataSource(temp_csv_file)], mock_repository)
    service.ingest_all()
    
    print(f"Save called {mock_repository.save.call_count} times")
    print(f"Call args: {mock_repository.save.call_args_list}")
```

## Future Testing Improvements

Potential enhancements:
- Property-based testing with Hypothesis
- Performance benchmarks
- Load testing with large datasets
- Concurrent ingestion tests
- Database integration tests
- API mocking for external sources
- Snapshot testing for data structures
- Mutation testing for coverage gaps

## Related Documentation

- [Ingestion Service Documentation](INGESTION_SERVICE.md)
- [Architecture Overview](ARCHITECTURE.md)
- [API Documentation](API.md)
