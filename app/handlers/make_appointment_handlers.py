import asyncio

from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

import app.keyboards.make_appointment_keyboards as kb
import app.keyboards.keyboards as user_kb
from app.utils.wix_api import post_availability, api_services_data, api_availability_data, fill_booking_data, create_booking, create_order


router = Router()

appointment = True
request_form = {}
temp_data = {}
step = False

class UserForm(StatesGroup):
    name = State()
    email = State()

@router.callback_query(F.data.startswith('register_service_'))
async def get_location(callback: types.CallbackQuery):
    service_index = int(callback.data.split('_')[-1])


    request_form['name'] = api_services_data[service_index]['name']
    request_form['service_Id'] = api_services_data[service_index]['id']
    await callback.message.edit_text(f'Виберіть локацію 🌍', reply_markup=await kb.choose_location(service_index))

@router.callback_query(F.data.startswith('location_service_'))
async def get_date(callback: types.CallbackQuery):
    service_location_id = callback.data.split('_')[-1]

    await post_availability(request_form['service_Id'], service_location_id)
    await callback.message.edit_text(f'Виберіть дату 📅', reply_markup=await kb.choose_date(api_availability_data))

@router.callback_query(F.data.startswith('day_'))
async def get_time(callback: types.CallbackQuery):
    start_date = callback.data.split('_')[-1].split('T')[0]

    await callback.message.edit_text('Виберіть час ⏲', reply_markup=await kb.choose_time(start_date, api_availability_data))

@router.callback_query(F.data.startswith('hour_'))
async def get_hour(callback: types.CallbackQuery):
    start_date = callback.data.split('_')[-1]
    request_form['slot'] = start_date

    for slot in api_availability_data:
        if start_date == slot['startDate']:
            await callback.message.edit_text('Ви є військовим?', reply_markup=await kb.is_soldier())

@router.callback_query(F.data.startswith('is_soldier_'))
async def get_price_agree(callback: types.CallbackQuery, state: FSMContext):
    for slot in api_availability_data:
        if request_form['slot'] == slot['startDate']:
            request_form['slot'] = slot

    soldier = callback.data.split('_')[-1]
    request_form['soldier'] = soldier

    await callback.message.edit_text("Введіть ваше ім'я:")
    await state.set_state(UserForm.name)

@router.message(UserForm.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введіть ваш Email:")
    await state.set_state(UserForm.email)

@router.message(UserForm.email)
async def process_surname(message: types.Message, state: FSMContext):
    await state.update_data(surname=message.text)
    user_data = await state.get_data()

    request_form["firstName"] = user_data.get("name")
    request_form["email"] = user_data.get("surname")

    await fill_booking_data('slot', request_form)

    status_booking = await create_booking(request_form['name'], request_form['slot'], request_form['firstName'], request_form['email'])

    if status_booking == 200:
        await message.answer(f"Дані успішно збережені", reply_markup=user_kb.main)
    else:
        await message.answer(f'Щось пішло не так 😢', reply_markup=user_kb.main)
        await message.answer(f'Ви ввели дані невірно, спробуйте знову!', reply_markup=user_kb.main)
    await state.clear()
