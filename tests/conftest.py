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
from src.domain.posts.use_cases.create_post import CreatePostUseCase
from src.domain.categories.use_cases.create_category import CreateCategoryUseCase
from src.schemas.users import UserCreate, UserUpdate
from src.schemas.posts import PostCreate
from src.schemas.categories import CategoryCreate


from jose import jwt
from src.services.auth import SECRET_AUTH_KEY, AUTH_ALGORITHM


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
async def db_session(db_url):
    engine = create_async_engine(db_url)
    SessionFactory = async_sessionmaker(
        bind=engine,
        expire_on_commit=False,
        class_=AsyncSession,
    )
    session = SessionFactory()
    await session.begin()
    yield session
    await session.rollback()
    await session.close()


@pytest_asyncio.fixture
async def async_client(db_url, sync_engine, db_session):
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url=f"http://test{settings.API_ROOT}"
    ) as ac:
        yield ac

    app.dependency_overrides.clear()


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
            user_create=UserCreate(login="alice", password="password"),
        )
        await session.commit()
    return user


@pytest_asyncio.fixture
async def alice_client(async_client, alice):
    token = jwt.encode(
        claims={"sub": alice.login},
        key=SECRET_AUTH_KEY.get_secret_value(),
        algorithm=AUTH_ALGORITHM,
    )
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url=f"http://test{settings.API_ROOT}"
    ) as ac:
        ac.headers["Authorization"] = f"Bearer {token}"
        yield ac


@pytest_asyncio.fixture(scope="session")
async def new_alice():
    yield UserUpdate(login="notsoalice", password="password2")


@pytest_asyncio.fixture(scope="session")
async def bob(sync_engine, db_url):
    engine = create_async_engine(db_url)
    async with async_sessionmaker(
        bind=engine,
        expire_on_commit=False,
        class_=AsyncSession,
    )() as session:
        use_case = CreateUserUseCase()
        user = await use_case.execute(
            session=session,
            user_create=UserCreate(login="bob", password="password"),
        )
        await session.commit()
    return user


@pytest_asyncio.fixture
async def bob_client(async_client, bob):
    token = jwt.encode(
        claims={"sub": bob.login},
        key=SECRET_AUTH_KEY.get_secret_value(),
        algorithm=AUTH_ALGORITHM,
    )
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url=f"http://test{settings.API_ROOT}"
    ) as ac:
        ac.headers["Authorization"] = f"Bearer {token}"
        yield ac


@pytest_asyncio.fixture(scope="session")
async def alice_category(db_url, alice):
    engine = create_async_engine(db_url)
    async with async_sessionmaker(
        bind=engine,
        expire_on_commit=False,
        class_=AsyncSession,
    )() as session:
        use_case = CreateCategoryUseCase()
        category = await use_case.execute(
            session=session,
            category_create=CategoryCreate(
                title="Alice's Category",
                description="Category Description",
                is_published=True,
                author_id=alice.id,
            ),
            current_user=alice,
        )
        await session.commit()
    return category


@pytest_asyncio.fixture(scope="session")
async def alice_post(sync_engine, db_url, alice, alice_category):
    engine = create_async_engine(db_url)
    async with async_sessionmaker(
        bind=engine,
        expire_on_commit=False,
        class_=AsyncSession,
    )() as session:
        use_case = CreatePostUseCase()
        post = await use_case.execute(
            session=session,
            post_create=PostCreate(
                title="Alice's Post",
                body="Post Description",
                datetime_to_publish="2000-01-01T00:00:00Z",
                category_id=alice_category.id,
                author_id=alice.id,
            ),
            current_user=alice,
        )
        await session.commit()
    return post
