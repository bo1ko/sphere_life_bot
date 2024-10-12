from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile
from openpyxl import Workbook

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


#  Get cities stats
@router.message(Command('get_cities'), flags={'admin_required': True})
async def cmd_get_city(message: types.Message):
    cities_data = await rq.get_cities()
    
    cities_str = 'Місто'.ljust(15) + '| Кількість запитів\n'
    cities_str += '-' * 35 + '\n' 

    for city in cities_data:
        cities_str += f'{city.name.ljust(15)}| {str(city.count).rjust(15)}\n'
        
    await message.answer(f'<pre>{cities_str}</pre>')

@router.message(Command('export_cities'), flags={'admin_required': True})
async def cmd_export_cities(message: types.Message):
    cities_data = await rq.get_cities()
    
    wb = Workbook()
    ws = wb.active
    ws.title = "Cities Data"

    ws.append(['Місто', 'Кількість запитів'])

    for city in cities_data:
        ws.append([city.name, city.count])

    file_path = 'cities_data.xlsx'
    wb.save(file_path)

    await message.answer_document(FSInputFile(file_path))

#  Get users stats
@router.message(Command('get_users'), flags={'admin_required': True})
async def cmd_get_city(message: types.Message):
    users_data = await rq.get_users()
    
    users_str = 'Телеграм айді'.ljust(15) + '| Нікнейн\n'
    users_str += '-' * 35 + '\n' 

    for user in users_data:
        users_str += f'{str(user.tg_id).ljust(15)}| {str(user.username).rjust(15)}\n'
        
    await message.answer(f'<pre>{users_str}</pre>')

@router.message(Command('export_users'), flags={'admin_required': True})
async def cmd_export_cities(message: types.Message):
    users_data = await rq.get_users()
    
    wb = Workbook()
    ws = wb.active
    ws.title = "Users Data"

    ws.append(['Телеграм айді', 'Нікнейн'])

    for user in users_data:
        ws.append([user.tg_id, user.username])

    file_path = 'users_data.xlsx'
    wb.save(file_path)

    await message.answer_document(FSInputFile(file_path))
