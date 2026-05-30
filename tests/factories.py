import factory
from factory.alchemy import SQLAlchemyModelFactory

from app.models.accounts import Account


class BaseFactory(SQLAlchemyModelFactory):
    @classmethod
    def with_session(cls, session):
        cls._meta.sqlalchemy_session = session
        return cls


class AccountFactory(BaseFactory):
    class Meta:
        model = Account
        sqlalchemy_session = None

    name = factory.Faker('pystr', max_chars=15)
    balance = 150.00
