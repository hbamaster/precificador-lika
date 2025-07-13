# alembic/versions/20250715_initial.py
"""initial

Revision ID: 20250715_initial
Revises: 
Create Date: 2025-07-15 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = '20250715_initial'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Exemplo para tabela simples_nacional_faixa
    op.create_table(
        'simples_nacional_faixa',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('faturamento_inicio', sa.Float, nullable=False),
        sa.Column('faturamento_fim', sa.Float, nullable=False),
        sa.Column('aliquota', sa.Float, nullable=False),
        sa.Column('deducao', sa.Float, nullable=False),
    )
    op.create_table(
        'simples_nacional_reparticao',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('faixa_id', sa.Integer, sa.ForeignKey('simples_nacional_faixa.id'), unique=True),
        sa.Column('irpj', sa.Float, nullable=False),
        sa.Column('csll', sa.Float, nullable=False),
        sa.Column('cofins', sa.Float, nullable=False),
        sa.Column('pis', sa.Float, nullable=False),
        sa.Column('cpp', sa.Float, nullable=False),
        sa.Column('icms', sa.Float, nullable=False),
    )
    # ... repita para demais models

def downgrade():
    op.drop_table('simples_nacional_reparticao')
    op.drop_table('simples_nacional_faixa')
    # ... demais tables