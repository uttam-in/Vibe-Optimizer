"""
Ingestion orchestration service.
Single Responsibility: Coordinate data ingestion from multiple sources.
Dependency Inversion: Depends on IDataSource abstraction.
"""
from typing import List
from datetime import datetime

from src.core.interfaces import IDataSource, IRepository
from src.core.models import RawContent


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
        query: str, 
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
    
    def add_source(self, source: IDataSource):
        """Add a new data source dynamically."""
        self.sources.append(source)
    
    def remove_source(self, source_type: str):
        """Remove a data source."""
        self.sources = [s for s in self.sources if s.get_source_type().value != source_type]
