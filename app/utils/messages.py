from enum import StrEnum


class AlreadyExists(StrEnum):
    __complement = ' already exists'

    ACCOUNT = 'Account' + __complement


class DoesNotExist(StrEnum):
    __complement = ' does not exist'

    ACCOUNT = 'Account' + __complement


class AlreadyBeenDeleted(StrEnum):
    __complement = ' has already been deleted'

    ACCOUNT = 'The account' + __complement
