"""Superfície de imports que registra o modelo ORM em ``Base``.

Basta importar este módulo para que o autogenerate do Alembic enxergue
todas as classes mapeadas. Cada pacote de domínio adiciona seus modelos
aqui conforme são criados.
"""

from app.models.accounts import Account

__all__ = ['Account']
