from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid

class EmailLogOut(BaseModel):
    id: int
    smtp_account_id: int
    recipient_email: str
    subject: Optional[str]
    body: Optional[str]
    tracking_code: uuid.UUID
    message_id: Optional[str]
    status: str
    error_message: Optional[str]
    sent_at: datetime

    class Config:
        orm_mode = True