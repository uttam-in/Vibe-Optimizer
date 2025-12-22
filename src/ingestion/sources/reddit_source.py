"""
Reddit data source adapter.
Liskov Substitution: Can be used anywhere IDataSource is expected.
"""
from typing import List, Optional
from datetime import datetime

from src.core.interfaces import IDataSource
from src.core.models import RawContent, SourceType


class RedditSource(IDataSource):
    """Adapter for Reddit API."""
    
    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret
        # Initialize Reddit client here
    
    def fetch_content(
        self, 
        query: str, 
        since: Optional[datetime] = None,
        limit: int = 100
    ) -> List[RawContent]:
        """Fetch Reddit posts and comments matching query."""
        # Implementation: Use praw to fetch Reddit content
        pass
    
    def get_source_type(self) -> SourceType:
        return SourceType.REDDIT
