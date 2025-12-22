"""
Report generation implementation.
Single Responsibility: Generate formatted reports.
"""
from datetime import datetime
from typing import List

from src.core.interfaces import IReportGenerator, IRepository
from src.core.models import SentimentTrend, Insight


class HTMLReportGenerator(IReportGenerator):
    """Generates HTML reports."""
    
    def __init__(self, repository: IRepository):
        self.repository = repository
    
    def generate_report(
        self,
        start_date: datetime,
        end_date: datetime,
        format: str = "html"
    ) -> str:
        """Generate HTML report."""
        pass
