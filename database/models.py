import os

from sqlalchemy import BigInteger, String, DateTime, func, Text, Boolean, Integer
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
    tg_id: Mapped[BigInteger] = mapped_column(BigInteger) 
    username: Mapped[str] = mapped_column(String(52), nullable=True)
    is_admin: Mapped[Boolean] = mapped_column(Boolean, default=False, nullable=False)
    ask_city: Mapped[Boolean] = mapped_column(Boolean, default=False, nullable=False)
    ask_subscribe: Mapped[Boolean] = mapped_column(Boolean, default=False, nullable=False)

class Location(Base):
    __tablename__ = 'locations'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    city_name: Mapped[str] = mapped_column(String(64), nullable=False)
    city_name_ru: Mapped[str] = mapped_column(String(64), nullable=False)
    address: Mapped[str] = mapped_column(String(124), nullable=False)
    map_url: Mapped[str] = mapped_column(String(162), nullable=False)

class Service(Base):
    __tablename__ = 'services'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(124), nullable=False)
    short_desc: Mapped[str] = mapped_column(String(162), nullable=False)
    long_desc: Mapped[str] = mapped_column(Text, nullable=False)
    service_url: Mapped[str] = mapped_column(String(162), nullable=False)

class City(Base):
    __tablename__ = 'cities'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    count: Mapped[int] = mapped_column(Integer(), default=1)

class Media(Base):
    __tablename__ = 'media'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    media_name: Mapped[str] = mapped_column(String(150), nullable=False)
    media_link: Mapped[str] = mapped_column(String(150), nullable=False)

class QA(Base):
    __tablename__ = 'qa'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    question: Mapped[str] = mapped_column(Text, nullable=False)
    answer: Mapped[str] = mapped_column(Text, nullable=False)

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)