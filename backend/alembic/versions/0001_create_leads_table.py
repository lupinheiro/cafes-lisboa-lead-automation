"""create leads table

Revision ID: 0001
Revises:
Create Date: 2026-09-27

"""

import sqlalchemy as sa

from alembic import op

revision: str = "0001"
down_revision: str | None = None
branch_labels = None
depends_on = None

lead_status = sa.Enum(
    "new",
    "scored",
    "draft_ready",
    "pending_review",
    "approved",
    "sent",
    "rejected",
    "opted_out",
    name="leadstatus",
)


def upgrade() -> None:
    lead_status.create(op.get_bind(), checkfirst=True)
    op.create_table(
        "leads",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("place_id", sa.String(255), nullable=False, unique=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("business_type", sa.String(100), nullable=False),
        sa.Column("address", sa.String(500), nullable=True),
        sa.Column("phone", sa.String(50), nullable=True),
        sa.Column("website", sa.String(500), nullable=True),
        sa.Column("email", sa.String(255), nullable=True),
        sa.Column("rating", sa.Float(), nullable=True),
        sa.Column("score", sa.Float(), nullable=False, server_default="0"),
        sa.Column("status", lead_status, nullable=False, server_default="new"),
        sa.Column("outreach_draft", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_leads_place_id", "leads", ["place_id"])


def downgrade() -> None:
    op.drop_index("ix_leads_place_id", table_name="leads")
    op.drop_table("leads")
    lead_status.drop(op.get_bind(), checkfirst=True)
