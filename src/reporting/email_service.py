"""
Email notification service.
Single Responsibility: Handle email sending.
"""
from typing import List, Optional

from src.core.interfaces import INotificationService


class EmailService(INotificationService):
    """Email service using SendGrid."""
    
    def __init__(self, api_key: str, from_email: str):
        self.api_key = api_key
        self.from_email = from_email
    
    def send_email(
        self,
        to: List[str],
        subject: str,
        body: str,
        attachments: Optional[List[str]] = None
    ) -> bool:
        """Send email via SendGrid."""
        pass
