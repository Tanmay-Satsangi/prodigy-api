"""Add all column to programs table

Revision ID: bb62c7adaaa8
Revises: 8f9686c73e2d
Create Date: 2025-06-08 21:41:49.169182
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bb62c7adaaa8'
down_revision: Union[str, None] = '8f9686c73e2d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('username', sa.String, nullable=False, unique=True),
        sa.Column('email', sa.String, nullable=False, unique=True),
        sa.Column('address', sa.String, nullable=True),
        sa.Column('created_at', sa.DateTime, server_default=sa.text('(CURRENT_TIMESTAMP)')),
    )

    op.create_table(
        'programs',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('duration_days', sa.Integer, nullable=False),
        sa.Column('difficulty_level', sa.String, nullable=True),
        sa.Column('created_at', sa.DateTime, server_default=sa.text('(CURRENT_TIMESTAMP)')),
    )

    op.create_table(
        'activities',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('program_id', sa.Integer, sa.ForeignKey('programs.id')),
        sa.Column('title', sa.String, nullable=False),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('day_number', sa.Integer, nullable=False),
        sa.Column('duration_minutes', sa.Integer, nullable=False),
        sa.Column('category', sa.String, nullable=True),
    )

    op.create_table(
        'user_activity_completions',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id')),
        sa.Column('activity_id', sa.Integer, sa.ForeignKey('activities.id')),
        sa.Column('completed_at', sa.DateTime, server_default=sa.text('(CURRENT_TIMESTAMP)')),
        sa.Column('completion_date', sa.DateTime, nullable=False),
    )

    op.create_table(
        'user_progress',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id')),
        sa.Column('program_id', sa.Integer, sa.ForeignKey('programs.id')),
        sa.Column('start_date', sa.DateTime, nullable=False),
        sa.Column('current_day', sa.Integer, nullable=False),
        sa.Column('is_active', sa.Boolean, nullable=False),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('user_progress')
    op.drop_table('user_activity_completions')
    op.drop_table('activities')
    op.drop_table('programs')
    op.drop_table('users')
