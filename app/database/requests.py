from app.database.models import async_session
from app.database.models import User, Media, City, Location
from sqlalchemy import select, or_


async def set_user(tg_id: int, username: str):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id, username=username))
            await session.commit()

async def get_user(tg_id: int):
    async with async_session() as session:
        return await session.scalar(select(User).where(User.tg_id == tg_id))

async def add_admin(username: str):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.username == username))

        if user:
            user.is_admin = True
            await session.commit()

            return True
        else:
            return False

async def check_admin(tg_id: int):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if user and user.is_admin:
            return True
        else:
            return False

async def set_city(city_name: str):
    async with async_session() as session:
        city = await session.scalar(select(City).where(City.name == city_name))

        if not city:
            session.add(City(name=city_name))
        else:
            city.count += 1

        await session.commit()

async def update_ask_city(tg_id: int):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        user.ask_city = True
        
        await session.commit()

# async def set_location(city_name: str, city_name_ru: str, address: str, maps_url: str):
#     async with async_session() as session:
#         city = await session.scalar(select(City).where(City.name == city_name))

#         if not city:
#             session.add(City(
#                 city_name=city_name,
#                 city_name_ru=city_name_ru,
#                 address=address,
#                 maps_url=maps_url
#             ))
#             await session.commit()

async def get_locations():
    async with async_session() as session:
        return await session.scalars(select(Location))

async def get_location(city_name: str):
    async with async_session() as session:
        city_name = await session.scalar(
            select(Location).where(
                or_(
                    Location.city_name == city_name,
                    Location.city_name_ru == city_name
                )
            )
        )

        if city_name:
            return True
        else:
            return False

async def get_media():
    async with async_session() as session:
        return await session.scalars(select(Media))