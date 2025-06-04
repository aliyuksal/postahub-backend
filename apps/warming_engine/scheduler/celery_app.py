from dotenv import load_dotenv
import os
from pathlib import Path
from celery import Celery
from shared.models import *
from apps.api_server.models import *
from apps.warming_engine.models import WarmupStrategy

from sqlalchemy.orm import configure_mappers
configure_mappers()


# 📌 .env dosyasını smtp-warming/ klasöründen yükle
env_path = Path(__file__).resolve().parents[3] / ".env"
print(f"🔍 Yüklenen .env path: {env_path}")
load_dotenv(dotenv_path=env_path)

# ✅ Ortam değişkeni kontrolü
redis_url = os.getenv("REDIS_BROKER_URL")
if not redis_url:
    raise RuntimeError("❌ .env dosyası bulunamadı veya REDIS_BROKER_URL tanımlı değil")

print(f"✅ REDIS_BROKER_URL: {redis_url}")

# 🚀 Celery app oluşturuluyor
celery_app = Celery(
    "warmup_engine",
    broker=redis_url,
    backend=os.getenv("REDIS_BACKEND_URL", redis_url)  # Eğer ayrı backend istersen .env'e ekleyebilirsin
)

# 📦 Görevlerin bulunduğu modüller

celery_app.autodiscover_tasks(["apps.warming_engine"])

if __name__ == "__main__":
    celery_app.start()