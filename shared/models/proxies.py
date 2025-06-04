from sqlalchemy import Column, Integer, String, Boolean
from shared.database.base import Base

class Proxy(Base):
    __tablename__ = "proxies"

    id = Column(Integer, primary_key=True)
    host = Column(String)
    port = Column(Integer)
    username = Column(String, nullable=True)
    password = Column(String, nullable=True)
    used = Column(Boolean, default=False)