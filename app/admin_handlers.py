from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from app.keyboards import answer
from app.middlewares import AdminCheckMiddleware

import validators
import app.database.requests as rq


router = Router()
router.message.middleware(AdminCheckMiddleware())

class Admin(StatesGroup):
    add_user = State()
    remove_user = State()

class Media(StatesGroup):
    add_name = State()
    add_url = State()

    remove_name = State()

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

#  Add media
@router.message(Command('add_media'), flags={'admin_required': True})
async def cmd_add_media(message: types.Message, state: FSMContext):
    await message.answer('Введіть назву медіа:')
    await state.set_state(Media.add_name)

@router.message(Media.add_name)
async def add_media_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer('Тепер введіть URL:')
    await state.set_state(Media.add_url)

@router.message(Media.add_url)
async def add_media_url(message: types.Message, state: FSMContext):
    if not validators.url(message.text):
        await message.answer("Некоректний URL. Будь ласка, введіть правильний URL")
        await state.clear()
        return

    await state.update_data(url=message.text)

    media_data = await state.get_data()
    location_name = media_data['name']
    location_url = media_data['url']

    await message.answer(f"Медіа додано:\n\nНазва: {location_name}\nURL: {location_url}")
    await rq.add_media(location_name, location_url)
    await state.clear()

#  Remove media
@router.message(Command('remove_media'), flags={'admin_required': True})
async def cmd_remove_media(message: types.Message, state: FSMContext):
    await message.answer('Введіть назву медіа')
    await state.set_state(Media.remove_name)

@router.message(Media.remove_name)
async def remove_media_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    media_data = await state.get_data()
    media = await rq.remove_media(media_data["name"])

    if media:
        await message.answer(f'Медіа "{media_data["name"]}" видалено')
    else:
        await message.answer(f'Медіа "{media_data["name"]}" не існує')
