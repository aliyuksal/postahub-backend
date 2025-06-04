from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apps.api_server.core.database import engine, Base
from apps.api_server.routers.smtp_router import router as smtp_router
from apps.api_server.routers.auth_router import router as auth_router
from apps.api_server.routers.email_logs import router as email_logs_router
from apps.api_server.routers.smtp_summary import router as smtp_summary_router
from apps.api_server.routers.warmup_strategy import router as warmup_strategy_router
from apps.warming_engine.models.warmup_strategy import WarmupStrategy  # warmup_plan burada DailyWarmupPlan için olabilir
from dotenv import load_dotenv
from pathlib import Path
import os
from apps.api_server.routers import dashboard_router

from apps.api_server.models import user, smtp_account
from shared.models import email_logs, warmup_target, ai_prompt
from apps.warming_engine.models import warmup_strategy

# ⏳ Ortam değişkenlerini yükle (.env dosyası api_server içinde)
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

# 🔐 Ortamdan gelen JWT_SECRET'i kontrol et
jwt_secret = os.getenv("JWT_SECRET")
print(f"✅ JWT_SECRET Loaded: {jwt_secret[:5]}******" if jwt_secret else "❌ JWT_SECRET not loaded!")

# 🚀 Uygulama başlat
app = FastAPI()

# 🌐 CORS ayarları
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://postahub.com",
        "https://postahub-frontend.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 📦 Veritabanı tablolarını oluştur
@app.on_event("startup")
def startup():
    print("🔧 Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created successfully!")

# 🔗 Router kayıtları
app.include_router(auth_router)

app.include_router(smtp_summary_router)
app.include_router(smtp_router)

app.include_router(dashboard_router.router)
app.include_router(email_logs_router)
app.include_router(warmup_strategy_router)  # 👈 artık doğru isim

# 🔍 Basit sağlık kontrolü
@app.get("/")
def root():
    return {"status": "ok"}

@app.get("/api/smtp")
def smtp_status():
    return {"smtp": "active"}

