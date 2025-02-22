"""empty message

Revision ID: ad1765862e55
Revises: 
Create Date: 2021-07-21 15:55:40.936580

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'ad1765862e55'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'actors', 'movies', ['movie_id'], ['id'])
    op.alter_column('movies', 'release_date',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('movies', 'release_date',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.drop_constraint(None, 'actors', type_='foreignkey')
    # ### end Alembic commands ###
