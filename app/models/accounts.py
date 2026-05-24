from decimal import Decimal

from sqlalchemy import Boolean, Numeric, String, text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.mixins import IDMixin


class Account(Base, IDMixin):
    __tablename__ = 'accounts'

    name: Mapped[str] = mapped_column(String(15), nullable=False, unique=True)
    balance: Mapped[Decimal] = mapped_column(
        Numeric(10, 2), nullable=False, server_default=text('0.00')
    )
    deleted: Mapped[bool] = mapped_column(
        Boolean(), nullable=False, server_default=text('false')
    )
