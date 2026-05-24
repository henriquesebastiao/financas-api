import pytest
from sqlalchemy.exc import IntegrityError

from app.models import Account


async def test_create_account_on_db(db_session):
    account = Account(
        name='Nubank',
        balance=150.00,
    )

    db_session.add(account)
    await db_session.flush()
    await db_session.refresh(account)

    assert isinstance(account.id, int)
    assert account.deleted is False


async def test_create_account_on_db_without_name_error(db_session):
    account = Account(balance=150.00)
    db_session.add(account)

    with pytest.raises(IntegrityError):
        await db_session.flush()


async def test_create_account_on_db_without_balance(db_session):
    account = Account(name='MP')
    db_session.add(account)

    await db_session.flush()
    await db_session.refresh(account)

    assert account.balance == 0.00
