from sqlalchemy import Integer
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from config import config

engine = create_async_engine(config.DATABASE_URL, echo=True)

Session = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)