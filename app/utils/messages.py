from enum import StrEnum


class AlreadyExists(StrEnum):
    __complement = ' already exists'

    ACCOUNT = 'Account' + __complement
