"""agregar usuario_id a libros

Revision ID: 05d6187bbefe
Revises: 7f6818a9330f
Create Date: 2026-10-17 14:49:12.804079

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '05d6187bbefe'
down_revision: Union[str, Sequence[str], None] = '7f6818a9330f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table('libros', schema=None) as batch_op:
        batch_op.add_column(sa.Column('usuario_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key('fk_libros_usuario', 'usuarios', ['usuario_id'], ['id'])

def dowgrade() -> None:
    with op.batch_alter_table('libros', schema=None) as batch_op:
        batch_op.drop_constraint('fk_libros_usuario', type='foreingkey')
        batch_op.drop_column('usuario_id')