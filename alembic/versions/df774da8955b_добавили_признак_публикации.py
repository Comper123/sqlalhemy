"""добавили признак публикации

Revision ID: df774da8955b
Revises: 
Create Date: 2024-04-01 14:08:50.951282

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'df774da8955b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'departments', 'users', ['chief'], ['id'])
    op.add_column('users', sa.Column('city_from', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'city_from')
    op.drop_constraint(None, 'departments', type_='foreignkey')
    # ### end Alembic commands ###
