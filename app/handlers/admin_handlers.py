from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from app.middlewares import AdminCheckMiddleware
from app.utils.update_db import update_data

import app.database.requests as rq


router = Router()
router.message.middleware(AdminCheckMiddleware())

class Admin(StatesGroup):
    add_user = State()
    remove_user = State()

#  Add admin / Ask username
@router.message(Command('add_admin'), flags={'admin_required': True})
async def cmd_add_admin(message: types.Message, state: FSMContext):
    await message.answer('Введіть юзернейм користувача (без @)\nПриклад: andy, maria03')
    await state.set_state(Admin.add_user)

#  Add admin / Add admin rule
@router.message(Admin.add_user)
async def add_admin(message: types.Message, state: FSMContext):
    await state.update_data(username=message.text)
    admin_data = await state.get_data()
    admin = await rq.add_admin(admin_data['username'])

    if admin:
        await message.answer('Адміністратор доданий')
    else:
        await message.answer('Такого юзернейму не існує')

    await state.clear()

#  Remove admin
@router.message(Command('remove_admin'), flags={'admin_required': True})
async def cmd_remove_admin(message: types.Message, state: FSMContext):
    await message.answer('Введіть юзернейм користувача (без @)\nПриклад: andy, maria03')
    await state.set_state(Admin.remove_user)

#  Remove admin / Remove admin rule
@router.message(Admin.remove_user)
async def remove_admin(message: types.Message, state: FSMContext):
    await state.update_data(username=message.text)
    admin_data = await state.get_data()

    admin = await rq.remove_admin(admin_data['username'])

    if admin:
        await message.answer('Адміністратор видалений')
    else:
        await message.answer('Такого юзернейму не існує')

    await state.clear()

#  Show admin list
@router.message(Command('admin_list'), flags={'admin_required': True})
async def cmd_show_admin_list(message: types.Message, state: FSMContext):
    admin_list = await rq.admin_list()
    admin_str = ''

    for admin in admin_list:
        admin_str += f'@{admin.username}\n'

    await message.answer(f'Список адміністраторів:\n\n{admin_str}')

@router.message(Command('refresh'), flags={'admin_required': True})
async def cmd_refresh(message: types.Message):
    await update_data(message)

