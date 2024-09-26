from aiogram import F, Router
from aiogram import types
from aiogram.filters import CommandStart

import app.database.requests as rq
import app.keyboards as kb


router = Router()

@router.message()

@router.message(CommandStart())
async def cmd_start(message: types.Message):
    await rq.set_user(message.from_user.id)
    await message.answer('Hello', reply_markup=kb.main)
