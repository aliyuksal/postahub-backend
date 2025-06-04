from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

# Ortam değişkeninden bağlantı bilgisi
DATABASE_URL = os.getenv("DATABASE_URL")

# SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Model mirası için temel sınıf
Base = declarative_base()

# Dependency olarak kullanılacak DB oturumu
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()