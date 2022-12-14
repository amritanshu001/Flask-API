"""empty message

Revision ID: 436b8159efd5
Revises: 131825b03c35
Create Date: 2022-12-15 11:40:58.107306

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '436b8159efd5'
down_revision = '131825b03c35'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('store_item')
    op.drop_table('stores')
    op.drop_table('items')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('items',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('items_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('item_name', sa.VARCHAR(length=60), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='items_pkey'),
    sa.UniqueConstraint('item_name', name='items_item_name_key'),
    postgresql_ignore_search_path=False
    )
    op.create_table('stores',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('stores_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('store_name', sa.VARCHAR(length=60), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='stores_pkey'),
    sa.UniqueConstraint('store_name', name='stores_store_name_key'),
    postgresql_ignore_search_path=False
    )
    op.create_table('store_item',
    sa.Column('store_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('item_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['item_id'], ['items.id'], name='store_item_item_id_fkey'),
    sa.ForeignKeyConstraint(['store_id'], ['stores.id'], name='store_item_store_id_fkey'),
    sa.PrimaryKeyConstraint('store_id', 'item_id', name='store_item_pkey')
    )
    # ### end Alembic commands ###
