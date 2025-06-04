from sqlalchemy import Column, Integer, String, Boolean, Text
from shared.database.base import Base

class GmailProfile(Base):
    __tablename__ = "gmail_profiles"

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True)
    password = Column(String)
    recovery_email = Column(String, nullable=True)
    cookies = Column(Text, nullable=True)  # JSON string olarak
    user_agent = Column(String, nullable=True)