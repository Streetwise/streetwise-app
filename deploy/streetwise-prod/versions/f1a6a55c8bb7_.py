"""empty message

Revision ID: f1a6a55c8bb7
Revises: 4ee1be843d6e
Create Date: 2020-06-10 21:35:56.368627

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f1a6a55c8bb7'
down_revision = '4ee1be843d6e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('images_key_key', 'images', type_='unique')
    op.alter_column('sessions', 'agent_address',
               existing_type=sa.VARCHAR(length=32),
               type_=sa.String(length=64),
               existing_nullable=True)
    op.alter_column('sessions', 'agent_browser',
               existing_type=sa.VARCHAR(length=64),
               type_=sa.String(length=128),
               existing_nullable=True)
    op.alter_column('sessions', 'agent_platform',
               existing_type=sa.VARCHAR(length=64),
               type_=sa.String(length=128),
               existing_nullable=True)
    op.drop_constraint('sessions_campaign_id_fkey', 'sessions', type_='foreignkey')
    op.drop_column('sessions', 'campaign_id')
    op.add_column('votes', sa.Column('campaign_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'votes', 'campaign', ['campaign_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'votes', type_='foreignkey')
    op.drop_column('votes', 'campaign_id')
    op.add_column('sessions', sa.Column('campaign_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('sessions_campaign_id_fkey', 'sessions', 'campaign', ['campaign_id'], ['id'])
    op.alter_column('sessions', 'agent_platform',
               existing_type=sa.String(length=128),
               type_=sa.VARCHAR(length=64),
               existing_nullable=True)
    op.alter_column('sessions', 'agent_browser',
               existing_type=sa.String(length=128),
               type_=sa.VARCHAR(length=64),
               existing_nullable=True)
    op.alter_column('sessions', 'agent_address',
               existing_type=sa.String(length=64),
               type_=sa.VARCHAR(length=32),
               existing_nullable=True)
    op.create_unique_constraint('images_key_key', 'images', ['key'])
    # ### end Alembic commands ###
