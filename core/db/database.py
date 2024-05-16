from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)

from core.settings import config

engine = create_async_engine(url=config.database.db_url, echo=True)

async_session = async_sessionmaker(engine, class_=AsyncSession)
