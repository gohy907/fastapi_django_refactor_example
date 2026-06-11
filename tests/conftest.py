import pytest
import pytest_asyncio

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from testcontainers.postgres import PostgresContainer
from httpx import AsyncClient, ASGITransport

from main import app
from src.core.config import settings
from src.core.db import Base, get_db


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


@pytest_asyncio.fixture
async def async_client(db_url):
    engine = create_async_engine(db_url)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    SessionFactory = async_sessionmaker(
        bind=engine, expire_on_commit=False, class_=AsyncSession,
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
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()
