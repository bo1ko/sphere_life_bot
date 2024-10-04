from oauthlib.uri_validate import query

from app.database.models import async_session
from app.database.models import User, Media, City, Location, Service, QA
from sqlalchemy import select, delete, or_, BigInteger


async def set_user(tg_id: BigInteger, username: str):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if user:
            if user.username != username:
                user.username = username
                await session.commit()
        else:
            session.add(User(tg_id=tg_id, username=username))
            await session.commit()

        return user

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

async def remove_admin(username: str):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.username == username))

        if user:
            user.is_admin = False
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

async def admin_list():
    async with async_session() as session:
        return await session.scalars(select(User).where(User.is_admin == True))

async def get_services():
    async with async_session() as session:
        return await session.scalars(select(Service))

async def get_service(service_id: int):
    async with async_session() as session:
        return await session.scalar(select(Service).where(Service.id == service_id))

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

async def get_qa_set():
    async with async_session() as session:
        return await session.scalars(select(QA))

async def get_qa(qa_id: int):
    async with async_session() as session:
        return await session.scalar(select(QA).where(QA.id == qa_id))

async def get_media():
    async with async_session() as session:
        return await session.scalars(select(Media))

async def clear_tables():
    async with async_session() as session:
        async with session.begin():
            await session.execute(delete(Location))
            await session.execute(delete(Media))
            await session.execute(delete(QA))

        await session.commit()

async def add_media(name: str, url: str):
    async with async_session() as session:
        async with session.begin():
            session.add(Media(media_name=name, media_link=url))

        await session.commit()


async def add_qa(question: str, answer: str):
    async with async_session() as session:
        async with session.begin():
            session.add(QA(question=question, answer=answer))

        await session.commit()

async def add_location(city_name: str, city_name_ru: str, address: str, map_url: str):
    async with async_session() as session:
        async with session.begin():
            session.add(Location(city_name=city_name, city_name_ru=city_name_ru, address=address, map_url=map_url))

        await session.commit()
