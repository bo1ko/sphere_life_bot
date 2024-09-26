import os

from sqlalchemy import BigInteger, String, ForeignKey, DateTime, func, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from dotenv import load_dotenv


load_dotenv()
engine = create_async_engine(url=os.getenv('DB_URL'))
async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_id = mapped_column(BigInteger) 

class Admin(Base):
    __tablename__ = 'admins'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    admin_id = mapped_column(BigInteger)

class Media(Base):
    __tablename__ = 'media'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    media_name: Mapped[str] = mapped_column(String(150), nullable=False)
    media_desc: Mapped[str] = mapped_column(Text)
    media_link: Mapped[str] = mapped_column(String(150), nullable=False)

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)