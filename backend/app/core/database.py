from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from app.core.config import settings
from app.models.database import Base

# Create async engine
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    future=True,
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def init_db():
    """Initialize database tables."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        # create_all does not add columns to an existing SQLite database.
        # Keep old local MVP databases usable while assigning newly created
        # sessions to authenticated users.
        def add_owner_column(sync_conn):
            from sqlalchemy import inspect, text
            columns = {column["name"] for column in inspect(sync_conn).get_columns("research_sessions")}
            if "owner_id" not in columns:
                sync_conn.execute(text("ALTER TABLE research_sessions ADD COLUMN owner_id CHAR(32) REFERENCES users(id) ON DELETE CASCADE"))
            sync_conn.execute(text("CREATE INDEX IF NOT EXISTS ix_research_sessions_owner_id ON research_sessions (owner_id)"))
        await conn.run_sync(add_owner_column)

async def get_db() -> AsyncSession:
    """Dependency for getting DB session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
