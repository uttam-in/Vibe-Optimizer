# Ingestion Service Documentation

## Overview

The Ingestion Service is responsible for importing social media data from various sources into the Brand Sentiment Analysis system. It provides a flexible, extensible architecture for fetching content from multiple platforms and storing it in the repository.

## Architecture

The service follows SOLID principles with clear separation of concerns:

- **Single Responsibility**: Each component has one job (CSV reading, orchestration)
- **Dependency Inversion**: Depends on `IDataSource` and `IRepository` abstractions
- **Open/Closed**: Easy to extend with new data sources without modifying existing code

## Components

### CSVDataSource

A concrete implementation of `IDataSource` that reads social media data from CSV files.

#### Initialization

```python
from src.ingestion.ingestion_service import CSVDataSource
from src.core.models import SourceType

# Default source type (Twitter)
source = CSVDataSource("data/sentimentdataset.csv")

# Custom source type
source = CSVDataSource("data/reddit_posts.csv", SourceType.REDDIT)
```

#### Methods

**`fetch_content(query="", since=None, limit=100)`**

Fetches content from the CSV file with optional filtering.

Parameters:
- `query` (str): Text filter - searches within the Text column (case-insensitive)
- `since` (datetime): Fetch only content after this timestamp
- `limit` (int): Maximum number of items to return (default: 100)

Returns:
- `List[RawContent]`: List of parsed content objects

Example:
```python
from datetime import datetime

# Fetch all content
content = source.fetch_content()

# Fetch with text filter
workout_posts = source.fetch_content(query="workout")

# Fetch recent content
recent = source.fetch_content(since=datetime(2023, 1, 15, 16, 0, 0))

# Fetch limited results
limited = source.fetch_content(limit=10)

# Combine filters
filtered = source.fetch_content(
    query="park",
    since=datetime(2023, 1, 15, 0, 0, 0),
    limit=50
)
```

**`get_source_type()`**

Returns the `SourceType` enum for this data source.

#### CSV Format

Expected CSV columns:
- `Unnamed: 0` - Row ID
- `Text` - Post content (required)
- `Sentiment` - Sentiment label (Positive, Negative, Neutral)
- `Timestamp` - Post timestamp (format: `YYYY-MM-DD HH:MM:SS`)
- `User` - Author username
- `Platform` - Social media platform (Twitter, Instagram, Facebook, Reddit)
- `Hashtags` - Hashtags used in the post
- `Retweets` - Number of retweets/shares
- `Likes` - Number of likes/reactions
- `Country` - User's country
- `Year`, `Month`, `Day`, `Hour` - Timestamp components

#### Platform Mapping

The service maps platform strings to `SourceType` enums:
- `twitter` → `SourceType.TWITTER`
- `reddit` → `SourceType.REDDIT`
- `instagram` → `SourceType.TWITTER` (mapped for compatibility)
- `facebook` → `SourceType.TWITTER` (mapped for compatibility)

#### Data Validation

- Rows with invalid timestamps are skipped
- Empty or malformed numeric fields are converted to `None`
- Text fields are stripped of whitespace
- Missing authors default to `None`

### IngestionService

The orchestrator that coordinates data ingestion from multiple sources.

#### Initialization

```python
from src.ingestion.ingestion_service import IngestionService, CSVDataSource
from src.infrastructure.repository import InMemoryRepository

# Create sources
twitter_source = CSVDataSource("data/twitter.csv", SourceType.TWITTER)
reddit_source = CSVDataSource("data/reddit.csv", SourceType.REDDIT)

# Create repository
repository = InMemoryRepository()

# Initialize service
service = IngestionService(
    sources=[twitter_source, reddit_source],
    repository=repository
)
```

#### Methods

**`ingest_all(query="", since=None, limit_per_source=100)`**

Ingests content from all configured sources.

Parameters:
- `query` (str): Search query to filter content
- `since` (datetime): Fetch content after this timestamp
- `limit_per_source` (int): Maximum items per source (default: 100)

Returns:
- `List[RawContent]`: All ingested content from all sources

Features:
- Automatically saves content to the repository
- Continues processing if one source fails
- Logs errors to stdout

Example:
```python
# Ingest from all sources
all_content = service.ingest_all()

# Ingest with filters
filtered_content = service.ingest_all(
    query="brand",
    since=datetime(2023, 1, 1),
    limit_per_source=50
)
```

**`ingest_from_csv(csv_path, query="", since=None, limit=100)`**

Convenience method to ingest from a single CSV file without pre-creating a source.

Parameters:
- `csv_path` (str): Path to CSV file
- `query` (str): Text filter
- `since` (datetime): Date filter
- `limit` (int): Maximum items

Returns:
- `List[RawContent]`: Ingested content

Example:
```python
# Quick CSV ingestion
content = service.ingest_from_csv(
    "data/new_data.csv",
    query="product",
    limit=100
)
```

**`add_source(source)`**

Dynamically adds a new data source to the service.

Example:
```python
new_source = CSVDataSource("data/additional.csv")
service.add_source(new_source)
```

**`remove_source(source_type)`**

Removes all sources matching the given source type.

Parameters:
- `source_type` (str): Source type value (e.g., "twitter", "reddit")

Example:
```python
service.remove_source("twitter")
```

## Error Handling

The service implements robust error handling:

1. **File Not Found**: `CSVDataSource` raises `FileNotFoundError` if CSV doesn't exist
2. **Invalid Timestamps**: Rows with malformed timestamps are skipped silently
3. **Source Failures**: `ingest_all()` catches exceptions and continues with other sources
4. **Data Type Errors**: Safe conversion methods prevent crashes on bad data

## Usage Examples

### Basic Ingestion

```python
from src.ingestion.ingestion_service import IngestionService, CSVDataSource
from src.infrastructure.repository import InMemoryRepository
from src.core.models import SourceType

# Setup
repository = InMemoryRepository()
csv_source = CSVDataSource("data/sentimentdataset.csv")
service = IngestionService([csv_source], repository)

# Ingest all data
content = service.ingest_all()
print(f"Ingested {len(content)} items")
```

### Multi-Source Ingestion

```python
# Multiple sources
twitter = CSVDataSource("data/twitter.csv", SourceType.TWITTER)
reddit = CSVDataSource("data/reddit.csv", SourceType.REDDIT)

service = IngestionService([twitter, reddit], repository)

# Ingest from all sources
all_content = service.ingest_all(limit_per_source=100)
```

### Filtered Ingestion

```python
from datetime import datetime, timedelta

# Get recent positive mentions
since_date = datetime.now() - timedelta(days=7)
content = service.ingest_all(
    query="our brand",
    since=since_date,
    limit_per_source=200
)

# Filter by sentiment in application logic
positive = [
    item for item in content
    if 'positive' in item.metadata.get('sentiment', '').lower()
]
```

### Dynamic Source Management

```python
# Start with no sources
service = IngestionService([], repository)

# Add sources as needed
service.add_source(CSVDataSource("data/source1.csv"))
service.add_source(CSVDataSource("data/source2.csv"))

# Ingest
content = service.ingest_all()

# Remove a source
service.remove_source("twitter")
```

## Testing

Comprehensive test coverage is provided in `tests/test_ingestion_service_csv.py`. See [Testing Documentation](TESTING_INGESTION.md) for details.

## Future Enhancements

Potential improvements:
- Add support for JSON and XML data sources
- Implement streaming for large files
- Add progress callbacks for long-running ingestion
- Support for incremental updates
- Batch processing optimization
- Parallel source processing
- Data validation schemas
- Custom field mapping configuration

## Related Documentation

- [Architecture Overview](ARCHITECTURE.md)
- [API Documentation](API.md)
- [Testing Guide](TESTING_INGESTION.md)
