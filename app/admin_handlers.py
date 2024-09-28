from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

import app.database.requests as rq
import app.keyboards as kb


router = Router()

class Admin(StatesGroup):
    username = State()


#  Add admin / Ask username
@router.message(Command('add_admin'))
async def add_admin(message: types.Message, state: FSMContext):
    if await rq.check_admin(message.from_user.id):
        await state.set_state(Admin.username)
        await message.answer('Введіть юзернейм користувача (без @)\nПриклад: andy, maria03')

#  Add admin / Add admin rule
@router.message(Admin.username)
async def save_admin(message: types.Message, state: FSMContext):
    await state.update_data(username=message.text)
    admin_data = await state.get_data()
    admin = await rq.add_admin(admin_data['username'])

    if admin:
        await message.answer('Адміністратор доданий')
    else:
        await message.answer('Такого юзернейму не існує')
    
    await state.clear()

#  Add locations
# @router.message(Command('add_location'))
# async def add_location(message: types.Message, state: FSMContext):
#     if await rq.check_admin(message.from_user.id):
#         await state.set_state(Location.name)
#         await message.answer('Введіть ')