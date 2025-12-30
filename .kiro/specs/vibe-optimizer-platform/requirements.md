# Requirements Document

## Introduction

Vibe Optimizer is an NLP-powered brand intelligence platform that analyzes sentiment and topics from multiple data sources including social media (Twitter, Reddit), product reviews, support tickets, and forums. The system provides real-time sentiment analysis, trend detection, actionable insights, and automated reporting to help organizations monitor brand perception, identify emerging trends and risks, and generate actionable insights from customer feedback.

## Glossary

- **System**: The Vibe Optimizer platform
- **Content**: Text data ingested from external sources
- **Sentiment_Analyzer**: Component that classifies text sentiment
- **Data_Source**: External platform providing content (Twitter, Reddit, etc.)
- **Repository**: Data persistence layer
- **Insight**: Actionable business intelligence derived from analyzed content
- **Compound_Score**: Numerical sentiment value ranging from -1 (negative) to 1 (positive)
- **Intensity**: Measure of sentiment strength from 0 (weak) to 1 (strong)
- **Topic**: Identified theme or subject extracted from content
- **Dashboard**: Web-based visualization interface
- **API**: REST API for programmatic access
- **Report**: Formatted summary of sentiment analysis results

## Requirements

### Requirement 1: Multi-Source Data Ingestion

**User Story:** As a brand manager, I want to ingest content from multiple data sources, so that I can analyze sentiment across all customer touchpoints.

#### Acceptance Criteria

1. WHEN a CSV file path is provided, THE System SHALL parse the file and create RawContent objects
2. WHEN ingesting from CSV, THE System SHALL validate timestamp format as 'YYYY-MM-DD HH:MM:SS'
3. IF a CSV row has an invalid timestamp, THEN THE System SHALL skip that row and continue processing
4. WHEN a query parameter is provided, THE System SHALL filter content to only include text matching the query
5. WHEN a since parameter is provided, THE System SHALL only return content with timestamps after the specified date
6. WHEN a limit parameter is provided, THE System SHALL return at most that number of content items
7. WHERE multiple data sources are configured, THE System SHALL ingest from all sources independently
8. IF an error occurs with one data source, THEN THE System SHALL log the error and continue with remaining sources
9. WHEN content is ingested, THE System SHALL persist each item to the Repository
10. THE System SHALL support Twitter, Reddit, Reviews, Support_Tickets, and Forums as source types

### Requirement 2: Sentiment Analysis

**User Story:** As a data analyst, I want accurate sentiment classification of content, so that I can understand customer perception.

#### Acceptance Criteria

1. WHEN text is provided for analysis, THE Sentiment_Analyzer SHALL return a SentimentScore with label, confidence, and intensity
2. THE Sentiment_Analyzer SHALL classify sentiment as Positive, Negative, or Neutral
3. WHEN analyzing text, THE System SHALL calculate a confidence score between 0 and 1
4. WHEN analyzing text, THE System SHALL calculate an intensity score between 0 and 1
5. WHEN analyzing text, THE System SHALL calculate a Compound_Score between -1 and 1
6. WHERE a trained model exists, THE System SHALL load the model and vectorizer from disk
7. IF the model files do not exist, THEN THE System SHALL raise a RuntimeError
8. WHEN calculating intensity, THE System SHALL use the inverse of neutral probability scaled by confidence
9. WHEN calculating Compound_Score, THE System SHALL compute positive probability minus negative probability
10. THE System SHALL support multiple analyzer implementations (Trained, Transformer, VADER)

### Requirement 3: Model Training and Persistence

**User Story:** As a machine learning engineer, I want to train custom sentiment models on domain-specific data, so that I can improve classification accuracy.

#### Acceptance Criteria

1. WHEN training a model, THE System SHALL accept a dataset with text and sentiment labels
2. WHEN training completes, THE System SHALL persist the model to disk as a pickle file
3. WHEN training completes, THE System SHALL persist the vectorizer to disk as a pickle file
4. WHEN loading a model, THE System SHALL read both model and vectorizer files
5. IF model loading fails, THEN THE System SHALL raise a RuntimeError with error details
6. WHEN a model path is provided, THE System SHALL support paths with or without .pkl extension
7. THE System SHALL store trained models in the models/ directory
8. WHEN training completes, THE System SHALL output model performance metrics

### Requirement 4: Content Analysis Pipeline

**User Story:** As a system administrator, I want automated analysis of ingested content, so that sentiment data is always current.

#### Acceptance Criteria

1. WHEN raw content is provided, THE System SHALL analyze sentiment for each item
2. WHEN analyzing a batch of content, THE System SHALL extract topics from all texts
3. WHEN analyzing individual content, THE System SHALL assign relevant topics from the extracted topic list
4. WHEN analysis completes, THE System SHALL create an AnalyzedContent object with sentiment, topics, and entities
5. WHEN analysis completes, THE System SHALL persist the AnalyzedContent to the Repository
6. THE System SHALL record the processed_at timestamp for each analyzed item
7. WHERE topic extraction is configured, THE System SHALL identify keywords for each topic
8. WHERE topic extraction is configured, THE System SHALL calculate relevance scores for topics

### Requirement 5: Real-Time Dashboard Visualization

**User Story:** As a brand manager, I want a real-time dashboard showing sentiment trends, so that I can monitor brand perception at a glance.

#### Acceptance Criteria

1. WHEN the dashboard loads, THE System SHALL display key metrics including overall sentiment, total mentions, average confidence, and positive rate
2. WHEN displaying overall sentiment, THE System SHALL show Positive if positive count exceeds negative count
3. WHEN displaying overall sentiment, THE System SHALL show Negative if negative count exceeds positive count
4. WHEN displaying overall sentiment, THE System SHALL show Neutral if positive and negative counts are equal
5. WHEN data is loaded, THE System SHALL display a pie chart showing sentiment distribution
6. WHEN data is loaded, THE System SHALL display a line chart showing sentiment trends over time
7. WHEN data is loaded, THE System SHALL display a chart showing average compound score over time
8. WHEN data is loaded, THE System SHALL display mentions grouped by source type
9. WHEN data is loaded, THE System SHALL display sentiment breakdown by source
10. WHERE hashtags exist in metadata, THE System SHALL display the top 10 most frequent hashtags
11. WHEN a date range is selected, THE System SHALL filter content to only show items within that range
12. WHEN source types are selected, THE System SHALL filter content to only show items from those sources
13. WHEN a search query is entered, THE System SHALL filter content to only show items containing the query text
14. WHEN displaying recent mentions, THE System SHALL allow filtering by sentiment label
15. WHEN displaying a mention, THE System SHALL show full text, source, author, timestamp, sentiment details, and metadata

### Requirement 6: REST API for Sentiment Data

**User Story:** As a developer, I want a REST API to access sentiment data programmatically, so that I can integrate with other systems.

#### Acceptance Criteria

1. THE System SHALL provide a GET /sentiment/trends endpoint
2. WHEN calling /sentiment/trends, THE System SHALL accept optional start_date, end_date, and source_type parameters
3. WHEN calling /sentiment/trends, THE System SHALL return sentiment distribution and average intensity for each time period
4. THE System SHALL provide a GET /sentiment/distribution endpoint
5. WHEN calling /sentiment/distribution, THE System SHALL return counts of positive, neutral, and negative sentiment
6. THE System SHALL provide a GET /insights/ endpoint
7. WHEN calling /insights/, THE System SHALL accept optional insight_type, severity, and limit parameters
8. THE System SHALL provide a GET /insights/{insight_id} endpoint
9. WHEN calling /insights/{insight_id}, THE System SHALL return detailed information for the specified insight
10. THE System SHALL provide a POST /reports/generate endpoint
11. WHEN calling /reports/generate, THE System SHALL accept start_date, end_date, and format parameters
12. THE System SHALL provide a GET /reports/latest endpoint
13. WHEN calling /reports/latest, THE System SHALL return the most recently generated report

### Requirement 7: Insight Generation

**User Story:** As a business analyst, I want automated insight generation from sentiment data, so that I can identify actionable trends and risks.

#### Acceptance Criteria

1. WHEN generating insights, THE System SHALL analyze sentiment trends over the specified time window
2. WHEN a sentiment drop exceeds the configured threshold, THE System SHALL generate a risk insight
3. WHEN a negative sentiment spike exceeds the configured threshold, THE System SHALL generate a critical risk insight
4. WHEN a topic frequency exceeds the configured threshold, THE System SHALL generate a trend insight
5. WHEN generating an insight, THE System SHALL include a title, description, insight_type, and severity
6. WHEN generating an insight, THE System SHALL include supporting_data with relevant metrics
7. WHEN generating an insight, THE System SHALL include actionable_recommendations
8. THE System SHALL support insight types: trend, risk, opportunity, and complaint
9. THE System SHALL support severity levels: low, medium, high, and critical
10. WHEN insights are generated, THE System SHALL persist them to the Repository

### Requirement 8: Report Generation and Distribution

**User Story:** As a marketing director, I want automated weekly email reports, so that I can stay informed without manual data gathering.

#### Acceptance Criteria

1. WHEN generating a report, THE System SHALL accept start_date and end_date parameters
2. WHEN generating a report, THE System SHALL support HTML and PDF formats
3. WHEN generating an HTML report, THE System SHALL include sentiment trends, distribution, and key insights
4. WHEN generating a report, THE System SHALL query the Repository for data within the specified date range
5. THE System SHALL provide email notification capability
6. WHEN sending an email, THE System SHALL accept recipient list, subject, body, and optional attachments
7. WHERE SendGrid is configured, THE System SHALL use SendGrid for email delivery
8. WHEN email sending fails, THEN THE System SHALL return false and log the error
9. WHEN email sending succeeds, THEN THE System SHALL return true

### Requirement 9: Data Persistence and Repository Pattern

**User Story:** As a system architect, I want a clean separation between business logic and data storage, so that the system is maintainable and testable.

#### Acceptance Criteria

1. THE System SHALL implement the Repository pattern for all data persistence operations
2. WHEN saving an entity, THE Repository SHALL return the entity ID
3. WHEN retrieving by ID, THE Repository SHALL return the entity if found or None if not found
4. WHEN finding entities, THE Repository SHALL accept a filters dictionary
5. WHEN finding entities, THE Repository SHALL return a list of matching entities
6. WHEN deleting an entity, THE Repository SHALL return true if successful or false if not found
7. THE System SHALL support both PostgreSQL and SQLite databases
8. WHERE SQLAlchemy is used, THE System SHALL define database models separate from domain models
9. THE System SHALL use Alembic for database migrations

### Requirement 10: Extensibility and SOLID Principles

**User Story:** As a software engineer, I want the system to follow SOLID principles, so that I can easily extend functionality without modifying existing code.

#### Acceptance Criteria

1. WHEN adding a new data source, THE System SHALL only require implementing the IDataSource interface
2. WHEN adding a new sentiment analyzer, THE System SHALL only require implementing the ISentimentAnalyzer interface
3. WHEN adding a new topic extractor, THE System SHALL only require implementing the ITopicExtractor interface
4. THE System SHALL depend on abstractions (interfaces) not concrete implementations
5. WHERE a service requires a sentiment analyzer, THE System SHALL accept any ISentimentAnalyzer implementation
6. WHERE a service requires a data source, THE System SHALL accept any IDataSource implementation
7. WHEN swapping analyzer implementations, THE System SHALL function without code changes to dependent services
8. THE System SHALL define all interfaces in the core/interfaces module
9. THE System SHALL define all domain models in the core/models module
10. THE System SHALL ensure core modules have no external dependencies

### Requirement 11: Configuration and Environment Management

**User Story:** As a DevOps engineer, I want centralized configuration management, so that I can deploy the system across different environments.

#### Acceptance Criteria

1. THE System SHALL load configuration from environment variables
2. THE System SHALL provide a .env.example file with all required configuration keys
3. WHERE a .env file exists, THE System SHALL load values from it
4. THE System SHALL use pydantic-settings for configuration validation
5. THE System SHALL store configuration in the config/settings.py module
6. THE System SHALL support configuration for database connection, API keys, email service, and model paths
7. WHERE required configuration is missing, THE System SHALL raise a validation error on startup

### Requirement 12: Testing and Quality Assurance

**User Story:** As a quality assurance engineer, I want comprehensive test coverage, so that I can ensure system reliability.

#### Acceptance Criteria

1. THE System SHALL provide unit tests for all core components
2. THE System SHALL provide integration tests for end-to-end workflows
3. WHEN running tests, THE System SHALL use pytest as the test framework
4. THE System SHALL achieve at least 85% code coverage
5. THE System SHALL provide tests for CSV ingestion with valid and invalid data
6. THE System SHALL provide tests for sentiment analysis with various text inputs
7. THE System SHALL provide tests for model training and loading
8. THE System SHALL provide tests for dashboard data processing
9. THE System SHALL provide tests for API endpoints
10. WHERE tests require external dependencies, THE System SHALL use mocks or test doubles

### Requirement 13: Scheduling and Background Jobs

**User Story:** As a system administrator, I want automated scheduling of ingestion and reporting tasks, so that data is always current without manual intervention.

#### Acceptance Criteria

1. THE System SHALL support scheduled execution of ingestion jobs
2. THE System SHALL support scheduled execution of report generation jobs
3. WHERE APScheduler is configured, THE System SHALL use it for job scheduling
4. WHERE Celery is configured, THE System SHALL use it for distributed task execution
5. WHEN a scheduled job fails, THE System SHALL log the error and continue with the next scheduled execution
6. THE System SHALL support configurable job schedules (hourly, daily, weekly)
7. THE System SHALL provide a jobs module in the scheduler package

### Requirement 14: Error Handling and Logging

**User Story:** As a support engineer, I want comprehensive error logging, so that I can troubleshoot issues quickly.

#### Acceptance Criteria

1. WHEN an error occurs during ingestion, THE System SHALL log the error with source type and error details
2. WHEN an error occurs during analysis, THE System SHALL log the error and continue with remaining items
3. WHEN model loading fails, THE System SHALL raise an exception with descriptive error message
4. WHEN database operations fail, THE System SHALL log the error and raise an exception
5. WHEN API requests fail, THE System SHALL return appropriate HTTP status codes
6. THE System SHALL log all errors with timestamp, severity level, and context information
7. WHERE logging is configured, THE System SHALL write logs to both console and file

### Requirement 15: Performance and Scalability

**User Story:** As a system architect, I want the system to handle large volumes of data efficiently, so that it can scale with business growth.

#### Acceptance Criteria

1. WHEN ingesting large datasets, THE System SHALL process items in batches
2. WHEN analyzing content, THE System SHALL support parallel processing where possible
3. WHERE caching is beneficial, THE System SHALL cache frequently accessed data
4. WHEN loading dashboard data, THE System SHALL limit initial data load to prevent memory issues
5. WHEN displaying dashboard visualizations, THE System SHALL use efficient data aggregation
6. THE System SHALL support pagination for API endpoints returning large result sets
7. WHERE database queries are slow, THE System SHALL use appropriate indexes
