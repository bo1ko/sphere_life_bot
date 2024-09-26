from aiogram import Router, F, types
from aiogram.filters import CommandStart, Command, or_f

import app.database.requests as rq
import app.keyboards as kb


router = Router()

@router.message(CommandStart())
async def cmd_start(message: types.Message):
    await rq.set_user(message.from_user.id)
    await message.answer('Hello', reply_markup=kb.main)

@router.message(Command('menu'))
async def cmd_menu(message: types.Message):
    await message.answer('Ви перейшли в головне меню', reply_markup=kb.main)

@router.message(or_f(Command('our_media'), ('наші медіа' == F.text.lower())))
async def our_media(message: types.Message):
    await message.answer('Список наших медіа', reply_markup=await kb.media())
