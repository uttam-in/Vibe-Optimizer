"""
Review data source adapter (e.g., Google Reviews, Trustpilot).
Liskov Substitution: Can be used anywhere IDataSource is expected.
"""
from typing import List, Optional
from datetime import datetime

from src.core.interfaces import IDataSource
from src.core.models import RawContent, SourceType


class ReviewSource(IDataSource):
    """Adapter for review platforms."""
    
    def __init__(self, api_key: str, platform: str = "google"):
        self.api_key = api_key
        self.platform = platform
        # Initialize review platform client here
    
    def fetch_content(
        self, 
        query: str, 
        since: Optional[datetime] = None,
        limit: int = 100
    ) -> List[RawContent]:
        """Fetch reviews matching query."""
        # Implementation: Fetch reviews from platform API
        pass
    
    def get_source_type(self) -> SourceType:
        return SourceType.REVIEWS
