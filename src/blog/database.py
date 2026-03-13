from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

# sqlalchemy_uri_sync = 'sqlite:///.blog.db'
sqlalchemy_uri_Async_driver = 'sqlite+aiosqlite:///.blog.db'


# engine = create_engine(sqlalchemy_uri_sync, connect_args={
#     'check_same_thread': False})

engine = create_async_engine(sqlalchemy_uri_Async_driver, echo=True)


# sessionlocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Async_sessionlocal = async_sessionmaker(bind=engine, expire_on_commit=False)

Base = declarative_base()


# def get_db():
#     db = sessionlocal()
#     try:
#         yield db
#     finally:
#         db.close()


async def get_db():
    async with Async_sessionlocal() as db:
        yield db


async def init_db():
    """ initializes the database """
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
