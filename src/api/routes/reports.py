"""
Reports API endpoints.
"""
from fastapi import APIRouter
from datetime import datetime

router = APIRouter()


@router.post("/generate")
def generate_report(
    start_date: datetime,
    end_date: datetime,
    format: str = "html"
):
    """Generate a report for the specified period."""
    pass


@router.get("/latest")
def get_latest_report():
    """Get the most recent report."""
    pass
