"""
Ingestion orchestration service.
Single Responsibility: Coordinate data ingestion from multiple sources.
Dependency Inversion: Depends on IDataSource abstraction.
"""
from typing import List, Optional
from datetime import datetime
import csv
import os

from src.core.interfaces import IDataSource, IRepository
from src.core.models import RawContent, SourceType


class CSVDataSource(IDataSource):
    """CSV file data source implementation."""
    
    def __init__(self, csv_path: str, source_type: SourceType = SourceType.TWITTER):
        """
        Initialize CSV data source.
        
        Args:
            csv_path: Path to the CSV file
            source_type: Type of source (default: TWITTER)
        """
        self.csv_path = csv_path
        self.source_type = source_type
        
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"CSV file not found: {csv_path}")
    
    def fetch_content(
        self, 
        query: str = "", 
        since: Optional[datetime] = None,
        limit: int = 100
    ) -> List[RawContent]:
        """
        Fetch content from CSV file.
        
        Args:
            query: Optional text filter (searches in Text column)
            since: Fetch content since this timestamp
            limit: Max items to fetch
            
        Returns:
            List of RawContent objects
        """
        content_list = []
        
        with open(self.csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                # Parse timestamp
                timestamp_str = row.get('Timestamp', '').strip()
                try:
                    timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
                except (ValueError, AttributeError):
                    # Skip rows with invalid timestamps
                    continue
                
                # Filter by date if specified
                if since and timestamp < since:
                    continue
                
                # Filter by query if specified
                text = row.get('Text', '').strip()
                if query and query.lower() not in text.lower():
                    continue
                
                # Map platform to SourceType
                platform = row.get('Platform', '').strip().lower()
                source_type = self._map_platform_to_source_type(platform)
                
                # Create RawContent object
                raw_content = RawContent(
                    id=row.get('Unnamed: 0', str(len(content_list))),
                    source_type=source_type,
                    content=text,
                    author=row.get('User', '').strip() or None,
                    timestamp=timestamp,
                    metadata={
                        'sentiment': row.get('Sentiment', '').strip(),
                        'platform': platform,
                        'hashtags': row.get('Hashtags', '').strip(),
                        'retweets': self._safe_float(row.get('Retweets')),
                        'likes': self._safe_float(row.get('Likes')),
                        'country': row.get('Country', '').strip(),
                        'year': row.get('Year', ''),
                        'month': row.get('Month', ''),
                        'day': row.get('Day', ''),
                        'hour': row.get('Hour', '')
                    },
                    url=None
                )
                
                content_list.append(raw_content)
                
                # Respect limit
                if len(content_list) >= limit:
                    break
        
        return content_list
    
    def get_source_type(self) -> SourceType:
        """Return the source type identifier."""
        return self.source_type
    
    def _map_platform_to_source_type(self, platform: str) -> SourceType:
        """Map platform string to SourceType enum."""
        platform_mapping = {
            'twitter': SourceType.TWITTER,
            'reddit': SourceType.REDDIT,
            'instagram': SourceType.TWITTER,  # Map Instagram to Twitter for now
            'facebook': SourceType.TWITTER,   # Map Facebook to Twitter for now
        }
        return platform_mapping.get(platform, SourceType.TWITTER)
    
    def _safe_float(self, value: str) -> Optional[float]:
        """Safely convert string to float."""
        try:
            return float(value) if value and value.strip() else None
        except (ValueError, AttributeError):
            return None


class IngestionService:
    """Orchestrates data ingestion from multiple sources."""
    
    def __init__(
        self, 
        sources: List[IDataSource],
        repository: IRepository
    ):
        self.sources = sources
        self.repository = repository
    
    def ingest_all(
        self, 
        query: str = "", 
        since: datetime = None,
        limit_per_source: int = 100
    ) -> List[RawContent]:
        """
        Ingest content from all configured sources.
        
        Args:
            query: Search query/brand name
            since: Fetch content since this timestamp
            limit_per_source: Max items per source
            
        Returns:
            List of ingested raw content
        """
        all_content = []
        
        for source in self.sources:
            try:
                content = source.fetch_content(query, since, limit_per_source)
                
                # Save to repository
                for item in content:
                    self.repository.save(item)
                
                all_content.extend(content)
                
            except Exception as e:
                # Log error and continue with other sources
                print(f"Error ingesting from {source.get_source_type()}: {e}")
        
        return all_content
    
    def ingest_from_csv(
        self,
        csv_path: str,
        query: str = "",
        since: datetime = None,
        limit: int = 100
    ) -> List[RawContent]:
        """
        Convenience method to ingest from a CSV file.
        
        Args:
            csv_path: Path to CSV file
            query: Optional text filter
            since: Fetch content since this timestamp
            limit: Max items to fetch
            
        Returns:
            List of ingested raw content
        """
        csv_source = CSVDataSource(csv_path)
        content = csv_source.fetch_content(query, since, limit)
        
        # Save to repository
        for item in content:
            self.repository.save(item)
        
        return content
    
    def add_source(self, source: IDataSource):
        """Add a new data source dynamically."""
        self.sources.append(source)
    
    def remove_source(self, source_type: str):
        """Remove a data source."""
        self.sources = [s for s in self.sources if s.get_source_type().value != source_type]
