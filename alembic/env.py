from shared.database.base import Base

import os
import sys
from dotenv import load_dotenv

# Alembic dosyasının bulunduğu yerden 2 seviye yukarı çık (project root)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, BASE_DIR)

# Ortam değişkenlerini yükle (opsiyonel)
load_dotenv(os.path.join(BASE_DIR, '.env'))

# 🔥 Doğrudan model sınıflarını import et
from apps.api_server.models.user import User
from apps.api_server.models.smtp_account import SMTPAccount
from shared.models import *
from apps.warming_engine.models.warmup_strategy import WarmupStrategy
from apps.api_server.models.subscription_plan import SubscriptionPlan
from shared.models.email_logs import EmailLog
from shared.models.engagement_logs import EngagementLog
from shared.models.campaigns import Campaign
from shared.models import *
from apps.api_server.models import *
from apps.warming_engine.models import WarmupStrategy

from sqlalchemy.orm import configure_mappers
configure_mappers()
from shared.models.ai_prompt import AIPrompt
from shared.models.gmail_profiles import GmailProfile
from shared.models.proxies import Proxy
from shared.models.warmup_target import WarmupTarget
from shared.models.mail_threads import MailThread

from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
load_dotenv(os.path.join(project_root, ".env"))

config = context.config
config.set_main_option("sqlalchemy.url", os.getenv("DATABASE_URL"))

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()