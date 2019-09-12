"""Alter facebook_id length to utf8mb4 compatibility issue"""

revision = 'e8d522d38d3d'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.drop_constraint(
        'ix_fbauth_info_facebook_id',
        'fbauth_info',
        type_='unique'
    )
    op.alter_column(
        'fbauth_info', 'facebook_id',
        existing_type=sa.VARCHAR(length=255),
        type_=sa.VARCHAR(length=191),
        existing_nullable=False
    )
    op.create_unique_constraint(
        'ix_fbauth_info_facebook_id',
        'fbauth_info',
        ['facebook_id']
    )


def downgrade():
    op.drop_constraint(
        'ix_fbauth_info_facebook_id',
        'fbauth_info',
        type_='unique'
    )
    op.alter_column(
        'fbauth_info', 'facebook_id',
        existing_type=sa.VARCHAR(length=191),
        type_=sa.VARCHAR(length=255),
        existing_nullable=False
    )
    op.create_unique_constraint(
        'ix_fbauth_info_facebook_id',
        'fbauth_info',
        ['facebook_id']
    )

