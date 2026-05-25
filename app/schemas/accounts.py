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


class AccountUpdate(AccountBase):
    model_config = ConfigDict(extra='forbid')

    deleted: bool = Field(default=False)


class AccountList(BaseModel):
    model_config = ConfigDict(extra='forbid')

    accounts: list[AccountPublic]
