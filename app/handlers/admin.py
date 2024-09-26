from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackGame
from dotenv import load_dotenv

import os

import app.keyboards.reply as kb_reply
import app.database.requests as rq


load_dotenv()
admin_router = Router()

@admin_router.message(Command('admin'))
async def cmd_admin(message: Message):
    admin = await rq.get_admin(message.from_user.id)
    if admin.admin_id == message.from_user.id:
        await message.answer('Hello, admin!', reply_markup=kb_reply.admin_main)


@admin_router.message(F.text.lower() == 'вийти з адмінки')
async def exit_admin(message: Message):
    await message.answer('Ви вийшли з адмінки. Щоб ввійти назад, введіть /admin', reply_markup=kb_reply.user_main)