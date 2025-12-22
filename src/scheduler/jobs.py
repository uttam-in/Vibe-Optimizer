"""
Scheduled jobs for ingestion and reporting.
Single Responsibility: Define scheduled tasks.
"""
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta


class ScheduledJobs:
    """Manages scheduled background jobs."""
    
    def __init__(self):
        self.scheduler = BackgroundScheduler()
    
    def start(self):
        """Start all scheduled jobs."""
        # Ingestion job - every 30 minutes
        self.scheduler.add_job(
            self.run_ingestion,
            'interval',
            minutes=30,
            id='ingestion_job'
        )
        
        # Weekly report - every Monday at 9 AM
        self.scheduler.add_job(
            self.send_weekly_report,
            'cron',
            day_of_week='mon',
            hour=9,
            id='weekly_report'
        )
        
        self.scheduler.start()
    
    def run_ingestion(self):
        """Run data ingestion."""
        pass
    
    def send_weekly_report(self):
        """Generate and send weekly report."""
        pass
