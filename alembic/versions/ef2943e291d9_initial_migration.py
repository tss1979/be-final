"""Initial migration

Revision ID: ef2943e291d9
Revises: 
Create Date: 2024-10-20 22:55:58.009845

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ef2943e291d9'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('role',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.Enum('ADMIN', 'USER', name='roleenum'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_role_id'), 'role', ['id'], unique=False)
    op.create_table('snippet',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('title', sa.String(length=50), nullable=True),
    sa.Column('code', sa.String(length=256), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_snippet_id'), 'snippet', ['id'], unique=False)
    op.create_table('user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=256), nullable=False),
    sa.Column('email', sa.String(length=128), nullable=False),
    sa.Column('hashed_password', sa.String(length=1024), nullable=False),
    sa.Column('salt', sa.String(length=1024), nullable=False),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_id'), 'user', ['id'], unique=False)
    op.create_index(op.f('ix_user_salt'), 'user', ['salt'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_salt'), table_name='user')
    op.drop_index(op.f('ix_user_id'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_snippet_id'), table_name='snippet')
    op.drop_table('snippet')
    op.drop_index(op.f('ix_role_id'), table_name='role')
    op.drop_table('role')
    # ### end Alembic commands ###
