import pytest
import pytest_asyncio

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from testcontainers.postgres import PostgresContainer
from httpx import AsyncClient, ASGITransport

from main import app
from src.core.config import settings
from src.core.db import Base, get_db

from src.domain.users.use_cases.create_user import CreateUserUseCase
from src.schemas.users import UserCreate


@pytest.fixture(scope="session")
def pg_container():
    with PostgresContainer("postgres:18.1") as pg:
        yield pg


@pytest.fixture(scope="session")
def db_url(pg_container):
    return (
        f"postgresql+asyncpg://{pg_container.username}:{pg_container.password}"
        f"@{pg_container.get_container_host_ip()}:{pg_container.get_exposed_port(5432)}"
        f"/{pg_container.dbname}"
    )


@pytest.fixture(scope="session")
def sync_engine(db_url):
    sync_url = db_url.replace("+asyncpg", "")
    engine = create_engine(sync_url)
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)


@pytest_asyncio.fixture
async def async_client(db_url, sync_engine):
    engine = create_async_engine(db_url)

    SessionFactory = async_sessionmaker(
        bind=engine,
        expire_on_commit=False,
        class_=AsyncSession,
    )

    async def override_get_db():
        session = SessionFactory()
        try:
            await session.begin()
            await session.begin_nested()
            yield session
        finally:
            await session.close()

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url=f"http://test{settings.API_ROOT}"
    ) as ac:
        yield ac

    app.dependency_overrides.clear()
    await engine.dispose()


@pytest_asyncio.fixture(scope="session")
async def alice(sync_engine, db_url):

    engine = create_async_engine(db_url)
    async with async_sessionmaker(
        bind=engine,
        expire_on_commit=False,
        class_=AsyncSession,
    )() as session:
        use_case = CreateUserUseCase()
        user = await use_case.execute(
            session=session,
            user_in=UserCreate(login="alice", password="password"),
        )
    await engine.dispose()
    return user


@pytest_asyncio.fixture
async def alice_client(async_client, alice):
    from jose import jwt
    from src.services.auth import SECRET_AUTH_KEY, AUTH_ALGORITHM

    token = jwt.encode(
        claims={"sub": alice.login},
        key=SECRET_AUTH_KEY.get_secret_value(),
        algorithm=AUTH_ALGORITHM,
    )
    async_client.headers["Authorization"] = f"Bearer {token}"
    yield async_client
