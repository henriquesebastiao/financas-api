from collections.abc import AsyncIterator
from pathlib import Path

import pytest
import pytest_asyncio
from alembic import command
from alembic.config import Config as AlembicConfig
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from testcontainers.postgres import PostgresContainer

from app.core.database import get_session
from app.main import app
from tests.factories import AccountFactory

_ALEMBIC_INI = Path(__file__).resolve().parent.parent / 'alembic.ini'


@pytest.fixture(scope='session')
def postgres_container():
    try:
        container = PostgresContainer(
            image='postgres:18.4-alpine',
            username='financas',
            password='financas',
            dbname='financas',
            driver='asyncpg',
        )
        container.start()
    except Exception as exc:
        pytest.skip(f'Docker/Postgres unavailable: {exc}')
    try:
        yield container
    finally:
        container.stop()


@pytest_asyncio.fixture(loop_scope='session', scope='session')
async def db_engine(
    postgres_container: PostgresContainer,
) -> AsyncIterator[AsyncEngine]:
    url = postgres_container.get_connection_url()
    engine = create_async_engine(url, future=True, pool_pre_ping=True)

    def _upgrade(sync_conn: object) -> None:
        alembic_cfg = AlembicConfig(str(_ALEMBIC_INI))
        alembic_cfg.attributes['connection'] = sync_conn
        command.upgrade(alembic_cfg, 'head')

    async with engine.begin() as connection:
        await connection.run_sync(_upgrade)

    try:
        yield engine
    finally:
        await engine.dispose()


@pytest_asyncio.fixture(loop_scope='session')
async def db_session(db_engine: AsyncEngine) -> AsyncIterator[AsyncSession]:
    session_factory = async_sessionmaker(
        bind=db_engine,
        expire_on_commit=False,
        autoflush=False,
    )
    async with session_factory() as session:
        try:
            yield session
        finally:
            await session.rollback()


@pytest.fixture
async def client(db_session: AsyncSession):
    async def get_session_override():
        yield db_session

    app.dependency_overrides[get_session] = get_session_override

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url='https://test'
    ) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture
async def account(db_session: AsyncSession):
    AccountFactory.with_session(db_session)
    account = AccountFactory()
    db_session.add(account)
    await db_session.commit()
    await db_session.refresh(account)
    return account
