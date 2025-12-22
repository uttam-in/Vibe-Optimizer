"""
Twitter data source adapter.
Liskov Substitution: Can be used anywhere IDataSource is expected.
"""
from typing import List, Optional
from datetime import datetime

from src.core.interfaces import IDataSource
from src.core.models import RawContent, SourceType


class TwitterSource(IDataSource):
    """Adapter for Twitter API."""
    
    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret
        # Initialize Twitter client here
    
    def fetch_content(
        self, 
        query: str, 
        since: Optional[datetime] = None,
        limit: int = 100
    ) -> List[RawContent]:
        """Fetch tweets matching query."""
        # Implementation: Use tweepy to fetch tweets
        pass
    
    def get_source_type(self) -> SourceType:
        return SourceType.TWITTER
