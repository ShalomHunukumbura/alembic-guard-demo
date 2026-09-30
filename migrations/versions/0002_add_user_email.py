"""add user email and link orders to users

Revision ID: 0002
Revises: 0001
Create Date: 2026-09-30
"""
from alembic import op
import sqlalchemy as sa

revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("users", sa.Column("email", sa.String(255), nullable=False))
    op.create_index("ix_users_email", "users", ["email"], unique=True)
    op.alter_column("users", "name", new_column_name="full_name")
    op.create_foreign_key("fk_orders_user", "orders", "users", ["user_id"], ["id"])


def downgrade() -> None:
    op.drop_constraint("fk_orders_user", "orders")
    op.alter_column("users", "full_name", new_column_name="name")
    op.drop_index("ix_users_email", "users")
    op.drop_column("users", "email")
