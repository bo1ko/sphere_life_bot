from app.database.models import async_session
from app.database.models import User, Media, City
from sqlalchemy import select


async def set_user(tg_id: int, username: str):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id, username=username))
            await session.commit()

async def set_city(city_name: str):
    async with async_session() as session:
        city = await session.scalar(select(City).where(City.name == city_name))

        if not city:
            session.add(City(name=city_name))
            await session.commit()

async def get_media():
    async with async_session() as session:
        return await session.scalars(select(Media))