from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select

from app.dependencies import SessionDep
from app.models.accounts import Account
from app.schemas.accounts import (
    AccountBase,
    AccountList,
    AccountPublic,
    AccountUpdate,
)
from app.utils.database import update_attributes
from app.utils.messages import AlreadyBeenDeleted, AlreadyExists, DoesNotExist

router = APIRouter(prefix='/accounts', tags=['accounts'])


@router.post(
    '',
    status_code=status.HTTP_201_CREATED,
    response_model=AccountPublic,
)
async def create(request: AccountBase, session: SessionDep):
    db_account = await session.scalar(
        select(Account).where(Account.name == request.name)
    )

    if db_account:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=AlreadyExists.ACCOUNT
        )

    db_account = Account(**request.model_dump())
    session.add(db_account)
    await session.commit()
    await session.refresh(db_account)

    return db_account


@router.patch(
    '/{account_id}',
    status_code=status.HTTP_200_OK,
    response_model=AccountPublic,
)
async def update(account_id: int, request: AccountUpdate, session: SessionDep):
    db_account = await session.scalar(
        select(Account).where(Account.id == account_id)
    )

    if not db_account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=DoesNotExist.ACCOUNT
        )

    db_account_check_name = await session.scalar(
        select(Account).where(Account.name == request.name)
    )

    if db_account_check_name:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=AlreadyExists.ACCOUNT
        )

    update_attributes(request, db_account)

    session.add(db_account)
    await session.commit()
    await session.refresh(db_account)

    return db_account


@router.delete(
    '/{account_id}',
    status_code=status.HTTP_200_OK,
    response_model=AccountPublic,
)
async def delete(account_id: int, session: SessionDep):
    db_account = await session.scalar(
        select(Account).where(Account.id == account_id)
    )

    if not db_account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=DoesNotExist.ACCOUNT
        )
    elif db_account.deleted is True:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=AlreadyBeenDeleted.ACCOUNT,
        )

    db_account.deleted = True

    session.add(db_account)
    await session.commit()
    await session.refresh(db_account)

    return db_account


@router.get(
    '/list', status_code=status.HTTP_200_OK, response_model=AccountList
)
async def list_accounts(session: SessionDep):
    db_accounts = await session.scalars(select(Account))
    return {'accounts': db_accounts.all()}
