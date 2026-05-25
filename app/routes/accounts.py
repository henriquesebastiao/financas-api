from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select

from app.dependencies import SessionDep
from app.models.accounts import Account
from app.schemas.accounts import AccountBase, AccountPublic
from app.utils.messages import AlreadyExists

router = APIRouter(prefix='/accounts', tags=['accounts'])


@router.post(
    '',
    status_code=status.HTTP_201_CREATED,
    response_model=AccountPublic,
)
async def create_account(request: AccountBase, session: SessionDep):
    db_account = await session.scalar(
        select(Account).where(Account.name == request.name)
    )

    if db_account:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=AlreadyExists.ACCOUNT
        )

    db_account = Account(**request.model_dump())
    session.add(db_account)
    await session.flush()
    await session.refresh(db_account)

    return db_account
