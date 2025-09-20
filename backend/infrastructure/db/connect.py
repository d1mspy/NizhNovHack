from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from settings.settings import settings
from sqlalchemy import create_engine
from persistent.db.base import Base
from sqlalchemy import DDL
from persistent.db.tables import SexEnum

def pg_connection() -> async_sessionmaker[AsyncSession]:
    
    engine = create_async_engine(
        f"postgresql+asyncpg://{settings.pg.username}:{settings.pg.password}@"
        f"{settings.pg.host}:{settings.pg.port}/{settings.pg.database}"
        )
    return async_sessionmaker(autocommit=False, autoflush=False, bind=engine)

def sync_create_tables() -> None:
    try:
        sync_engine = create_engine(
            f"postgresql://{settings.pg.username}:{settings.pg.password}@"
            f"{settings.pg.host}:{settings.pg.port}/{settings.pg.database}"
        )
        
        create_enum = DDL(
            "DO $$ "
            "BEGIN "
            "   IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'sex_enum') THEN "
            "       CREATE TYPE sex_enum AS ENUM ('male', 'female', 'other'); "
            "   END IF; "
            "END $$;"
        )
        
        with sync_engine.connect() as conn:
            conn.execute(create_enum)
            conn.commit()
        
        Base.metadata.create_all(sync_engine)
        sync_engine.dispose()
        print("Tables created successfully")
    except Exception as e:
        print(f"Error creating tables: {e}")