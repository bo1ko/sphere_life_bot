from aiogram import Router
from aiogram import types
from aiogram.filters import CommandStart

import app.database.requests as rq
import app.keyboards.reply as kb_reply


user_router = Router()

@user_router.message(CommandStart())
async def cmd_start(message: types.Message):
    await rq.set_user(message.from_user.id)
    await message.answer('Hello', reply_markup=kb_reply.user_main)
