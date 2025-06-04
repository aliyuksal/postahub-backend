from apps.api_server.models.smtp_account import SMTPAccount
from apps.api_server.models.user import User
from apps.warming_engine.models.warmup_strategy import WarmupStrategy
from shared.models.email_logs import EmailLog
from shared.models.ai_prompt import AIPrompt
from shared.models.warmup_target import WarmupTarget

from sqlalchemy.orm import configure_mappers
configure_mappers()