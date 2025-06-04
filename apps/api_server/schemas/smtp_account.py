from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class SMTPAccountCreate(BaseModel):
    provider: Optional[str] = Field(None, example="Gmail")
    email: EmailStr = Field(..., example="user@example.com")
    username: Optional[str] = Field(None, example="user@example.com")
    password: Optional[str] = Field(None, example="supersecret")
    host: Optional[str] = Field(None, example="smtp.gmail.com")
    port: Optional[int] = Field(None, example=587)
    use_tls: bool = Field(default=True)
    use_ssl: bool = Field(default=False)
    daily_limit: int = Field(default=100, example=50)
    status: Optional[str] = Field(default="active", example="active")
    reputation_score: int = Field(default=100, ge=0, le=100, example=100)


class SMTPAccountOut(SMTPAccountCreate):
    id: int

    class Config:
        from_attributes = True  # for ORM model -> pydantic v2 compatibility


class SMTPAccountUpdate(BaseModel):
    provider: Optional[str] = None
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: Optional[str] = None
    host: Optional[str] = None
    port: Optional[int] = None
    use_tls: Optional[bool] = None
    use_ssl: Optional[bool] = None
    daily_limit: Optional[int] = None
    status: Optional[str] = None
    reputation_score: Optional[int] = Field(None, ge=0, le=100)