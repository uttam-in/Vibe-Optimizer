"""
Sentiment API endpoints.
"""
from fastapi import APIRouter, Depends
from datetime import datetime
from typing import Optional

router = APIRouter()


@router.get("/trends")
def get_sentiment_trends(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    source_type: Optional[str] = None
):
    """Get sentiment trends over time."""
    pass


@router.get("/distribution")
def get_sentiment_distribution(
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
):
    """Get sentiment distribution (positive/neutral/negative)."""
    pass
