"""add created_at columns if missing

Revision ID: 0001_add_created_at_columns
Revises: 
Create Date: 2025-12-16 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0001_add_created_at_columns'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    inspector = sa.inspect(conn)

    # Add created_at to users
    users_cols = [c['name'] for c in inspector.get_columns('users')]
    if 'created_at' not in users_cols:
        op.add_column('users', sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False))

    # Add created_at to properties
    properties_cols = [c['name'] for c in inspector.get_columns('properties')]
    if 'created_at' not in properties_cols:
        op.add_column('properties', sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False))

    # Add created_at to bookings
    bookings_cols = [c['name'] for c in inspector.get_columns('bookings')]
    if 'created_at' not in bookings_cols:
        op.add_column('bookings', sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False))

    # Add created_at to payments
    payments_cols = [c['name'] for c in inspector.get_columns('payments')]
    if 'created_at' not in payments_cols:
        op.add_column('payments', sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False))


def downgrade():
    conn = op.get_bind()
    inspector = sa.inspect(conn)

    payments_cols = [c['name'] for c in inspector.get_columns('payments')]
    if 'created_at' in payments_cols:
        op.drop_column('payments', 'created_at')

    bookings_cols = [c['name'] for c in inspector.get_columns('bookings')]
    if 'created_at' in bookings_cols:
        op.drop_column('bookings', 'created_at')

    properties_cols = [c['name'] for c in inspector.get_columns('properties')]
    if 'created_at' in properties_cols:
        op.drop_column('properties', 'created_at')

    users_cols = [c['name'] for c in inspector.get_columns('users')]
    if 'created_at' in users_cols:
        op.drop_column('users', 'created_at')
