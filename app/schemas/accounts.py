from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class AccountBase(BaseModel):
    model_config = ConfigDict(extra='forbid')

    name: str = Field(min_length=1, max_length=15)
    balance: Decimal = Field(default=0.00)


class AccountPublic(AccountBase):
    model_config = ConfigDict(extra='forbid')

    id: int
    deleted: bool


class AccountUpdate(BaseModel):
    name: str | None = None
    balance: Decimal | None = None
    deleted: bool | None = None


class AccountList(BaseModel):
    model_config = ConfigDict(extra='forbid')

    accounts: list[AccountPublic]
