"""Add plan_name to WarmupStrategy

Revision ID: 3f401dc5b34b
Revises: 3288dd937cba
Create Date: 2025-05-23 01:36:19.060197

"""


from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from typing import Sequence, Union

# revision identifiers, used by Alembic.
revision: str = '3f401dc5b34b'
down_revision: Union[str, None] = '3288dd937cba'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('warmup_strategies', sa.Column('plan_name', sa.String(), nullable=False))
    op.add_column('warmup_strategies', sa.Column('sender_surname', sa.String(), nullable=True))
    op.add_column('warmup_strategies', sa.Column('email_language', sa.String(), nullable=True))
    op.add_column('warmup_strategies', sa.Column('email_template_type', sa.String(), nullable=False))
    op.add_column('warmup_strategies', sa.Column('esp_type', sa.String(), nullable=False))
    op.add_column('warmup_strategies', sa.Column('start_time', sa.Time(), nullable=False))
    op.add_column('warmup_strategies', sa.Column('end_time', sa.Time(), nullable=False))
    op.add_column('warmup_strategies', sa.Column('active_days', postgresql.ARRAY(sa.String()), nullable=False))
    op.add_column('warmup_strategies', sa.Column('reply_timing_strategy', sa.String(), nullable=False))
    op.add_column('warmup_strategies', sa.Column('updated_at', sa.DateTime(), nullable=True))
    op.alter_column('warmup_strategies', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('warmup_strategies', 'smtp_account_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('warmup_strategies', 'sender_name',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('warmup_strategies', 'sending_frequency',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.drop_column('warmup_strategies', 'language')
    op.drop_column('warmup_strategies', 'warmup_type')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('warmup_strategies', sa.Column('warmup_type', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('warmup_strategies', sa.Column('language', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.alter_column('warmup_strategies', 'sending_frequency',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('warmup_strategies', 'sender_name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('warmup_strategies', 'smtp_account_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('warmup_strategies', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.drop_column('warmup_strategies', 'updated_at')
    op.drop_column('warmup_strategies', 'reply_timing_strategy')
    op.drop_column('warmup_strategies', 'active_days')
    op.drop_column('warmup_strategies', 'end_time')
    op.drop_column('warmup_strategies', 'start_time')
    op.drop_column('warmup_strategies', 'esp_type')
    op.drop_column('warmup_strategies', 'email_template_type')
    op.drop_column('warmup_strategies', 'email_language')
    op.drop_column('warmup_strategies', 'sender_surname')
    op.drop_column('warmup_strategies', 'plan_name')
    # ### end Alembic commands ###
