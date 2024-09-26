import asyncio
import os
from ast import parse

from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types

from app.handlers import router
from app.database.models import async_main
from app.common.bot_cmds_list import private


load_dotenv()

async def main():
    await async_main()
    bot = Bot(token=os.getenv('TOKEN'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    dp = Dispatcher()
    dp.include_router(router)

    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
