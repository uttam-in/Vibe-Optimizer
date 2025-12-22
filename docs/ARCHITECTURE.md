# Architecture Overview

## SOLID Principles Implementation

### Single Responsibility Principle (SRP)
Each class has one reason to change:
- `SentimentAnalyzer`: Only sentiment analysis logic
- `TopicExtractor`: Only topic extraction logic
- `IngestionService`: Only orchestration of data ingestion
- `Repository`: Only data persistence operations

### Open/Closed Principle (OCP)
System is open for extension, closed for modification:
- New data sources can be added by implementing `IDataSource`
- New sentiment analyzers by implementing `ISentimentAnalyzer`
- No need to modify existing code

### Liskov Substitution Principle (LSP)
Implementations are interchangeable:
- Any `IDataSource` implementation (Twitter, Reddit, Reviews) can be used
- Any `ISentimentAnalyzer` (Transformer, VADER) can be swapped
- Services depend on interfaces, not concrete classes

### Interface Segregation Principle (ISP)
Focused, specific interfaces:
- `IDataSource`: Only data fetching methods
- `ISentimentAnalyzer`: Only sentiment analysis
- `ITopicExtractor`: Only topic operations
- No fat interfaces with unused methods

### Dependency Inversion Principle (DIP)
High-level modules depend on abstractions:
- `IngestionService` depends on `IDataSource`, not concrete sources
- `AnalysisService` depends on `ISentimentAnalyzer`, not specific analyzers
- Easy to test with mocks/stubs

## Data Flow

1. **Ingestion**: Sources → IngestionService → RawContentRepository
2. **Analysis**: RawContent → AnalysisService → AnalyzedContentRepository
3. **Insights**: AnalyzedContent → InsightGenerator → InsightRepository
4. **Reporting**: Data → ReportGenerator → EmailService
5. **Visualization**: Data → Dashboard/API

## Module Structure

- `core/`: Domain models and interfaces (no dependencies)
- `ingestion/`: Data source adapters
- `analysis/`: NLP processing
- `storage/`: Database and repositories
- `insights/`: Business logic for insights
- `reporting/`: Report generation and notifications
- `api/`: REST API endpoints
- `dashboard/`: Web UI
- `scheduler/`: Background jobs
