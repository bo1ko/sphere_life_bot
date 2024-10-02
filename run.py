import asyncio
import os

from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types

from app.handlers.user_handlers import router as user_router
from app.handlers.admin_handlers import router as admin_router
from app.handlers.make_appointment_handlers import router as make_appointment_router
from app.database.models import async_main
from app.common.bot_cmds_list import private

load_dotenv()

bot = Bot(token=os.getenv('TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))


async def main():
    await async_main()

    dp = Dispatcher()
    dp.include_router(user_router)
    dp.include_router(make_appointment_router)
    dp.include_router(admin_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
