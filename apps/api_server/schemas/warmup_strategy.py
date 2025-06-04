from pydantic import BaseModel
from datetime import time, datetime
from typing import List, Optional

class WarmupPlanCreate(BaseModel):
    smtp_account_id: int
    plan_name: Optional[str] = None  # boş bırakılabilir
    sender_name: str
    sender_surname: str
    email_language: str
    sending_frequency: int
    auto_increase_volume_percent: int
    email_template_type: str
    esp_type: str
    start_time: time
    end_time: time
    duration_days: int
    active_days: List[str]
    reply_timing_strategy: str
    prompt_type: Optional[str] = None  # 👈 yeni alan



class WarmupPlanOut(WarmupPlanCreate):
    id: int
    plan_name: str
    created_at: datetime
    updated_at: datetime
    prompt_type: Optional[str] = None

    class Config:
        orm_mode = True


class WarmupPlanUpdate(BaseModel):
    sender_name: Optional[str] = None
    sender_surname: Optional[str] = None
    email_language: Optional[str] = None
    sending_frequency: Optional[int] = None
    auto_increase_volume_percent: Optional[int] = None
    email_template_type: Optional[str] = None
    esp_type: Optional[str] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    duration_days: Optional[int] = None
    active_days: Optional[List[str]] = None
    reply_timing_strategy: Optional[str] = None
    prompt_type: Optional[str] = None  #