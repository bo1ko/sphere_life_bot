from aiogram import Router, F, types
from aiogram.filters import CommandStart, Command, or_f
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

import asyncio

from app.utils.handler_helpers import city_check, get_questions, send_questions_message, choose_payment_type
from app.utils.wix_api import api_services_data, fill_booking_data, clear_booking_data

import app.database.requests as rq
import app.keyboards.keyboards as kb


router = Router()

class City(StatesGroup):
    is_right = State()
    name = State()

class Admin(StatesGroup):
    username = State()


#  /start
@router.message(CommandStart())
async def cmd_start(message: types.Message):
    user = await rq.set_user(message.from_user.id, message.from_user.username)
    
    await message.answer('Ласкаво просимо до @spherelife_bot! 🤖')
    if not user.ask_subscribe:
        await asyncio.sleep(1)
        await message.answer('😊 Для початку рекомендуємо підписатися на наш телеграм-канал @spherelife 📲', reply_markup=kb.subscribe)
        
    else:
        await message.answer('Тут ви зможете дізнатся всю цікаву вам інформацію.', reply_markup=kb.main)
    

@router.callback_query(F.data == 'continue')
async def cmd_start_continue(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.message.answer('Тут ви зможете дізнатся всю цікаву вам інформацію.', reply_markup=kb.main)

#  Menu
@router.message(Command('menu'))
async def cmd_menu(message: types.Message):
    await message.answer('Ви перейшли в головне меню', reply_markup=kb.main)

#  Services
@router.message(or_f(Command('services'), ('список процедур' == F.text.lower())))
async def get_services(message: types.Message):
    await message.answer('📝 Список процедур 📝', reply_markup=await kb.service_list())

@router.callback_query(F.data == 'back_to_service_list')
async def get_services(callback: types.CallbackQuery):
    await clear_booking_data()
    await callback.message.edit_text('📝 Список процедур 📝', reply_markup=await kb.service_list())

@router.callback_query(F.data.startswith('service_'))
async def get_service(callback: types.CallbackQuery):
    service_index = int(callback.data.split('_')[1])
    price = await choose_payment_type(api_services_data, service_index)

    await fill_booking_data('fixed', False)

    if price[1] == 2:
        await fill_booking_data('price', 0)
        await callback.message.edit_text(
            f'<b>{api_services_data[service_index]['name']}</b>\n'
            f'<blockquote><i>{api_services_data[service_index]['tagLine']}</i></blockquote>'
            f'Ціна: {price[0]}\n',
            reply_markup=await kb.service_info(service_index))
    elif price[1] == 0:
        await fill_booking_data('price', price[0])
        await callback.message.edit_text(
            f'<b>{api_services_data[service_index]['name']}</b>\n'
            f'<blockquote><i>{api_services_data[service_index]['tagLine']}</i></blockquote>'
            f'Ціна: {price[0]} грн.\n'
            f'Військовим: {str(int(price[0]) / 2).split('.')[0]} грн.',
            reply_markup=await kb.service_info(service_index))
    elif price[1] == 1:
        await fill_booking_data('price', price[0])
        await fill_booking_data('fixed', True)
        await callback.message.edit_text(
            f'<b>{api_services_data[service_index]['name']}</b>\n'
            f'<blockquote><i>{api_services_data[service_index]['tagLine']}</i></blockquote>'
            f'Ціна: {price[0]} грн.\n',
            reply_markup=await kb.service_info(service_index))

@router.callback_query(F.data.startswith('more_info_'))
async def get_more_info(callback: types.CallbackQuery):
    service_index = int(callback.data.split('_')[-1])
    await callback.message.edit_text(f'<i><b>{api_services_data[service_index]['name']}</b></i>\n<blockquote><i>{api_services_data[service_index]['tagLine']}</i></blockquote>\n\n📝 Опис послуги 📝\n{api_services_data[service_index]['description']}', reply_markup=await kb.back_to_service_info(service_index))

#  Locations
@router.message(or_f(Command('locations'), ('наше місцезнаходження' == F.text.lower())))
async def get_city(message: types.Message, state: FSMContext):
    user = await rq.get_user(message.from_user.id)

    if user.ask_city:
        locations = await rq.get_locations()
        str_locations = await city_check(locations)
        await message.answer(str_locations, reply_markup=kb.main)
    else:
        await state.set_state(City.name) # branchLocation
        await message.answer('Введіть назву вашого міста')

#  Locations / Get city
@router.message(City.name)
async def check_city(message: types.Message, state: FSMContext):
    await state.update_data(city=message.text)
    city_data = await state.get_data()
    locations = await rq.get_locations()
    
    if await rq.get_location(city_data['city'].lower()):
        str_locations = await city_check(locations)
        await message.answer(str_locations, reply_markup=kb.main)
    else:
        await rq.update_ask_city(message.from_user.id)
        await rq.set_city(city_data['city'].lower())
        
        str_locations = await city_check(locations, '😔 На жаль, наших закладів ще немає у вашому місті 🌍\nМи врахували вашу відповідь, і як тільки відкриємося у вашому місті, повідомимо вас 📩\n\nОсь адреси, за якими ви можете нас знайти в інших містах 📍\n\n')

        await message.answer(str_locations, reply_markup=kb.main)

    await state.clear()

#  Questions&Answers
@router.message(or_f(Command('questions'), ('відповіді на питання' == F.text.lower())))
async def questions(message: types.Message):
    qa_set = await get_questions()
    await send_questions_message(message, qa_set)

#  Callback questions&answers
@router.callback_query(F.data == 'back_to_questions')
async def questions(callback: types.CallbackQuery):
    qa_set = await get_questions()
    await send_questions_message(callback, qa_set)

@router.callback_query(F.data.startswith('qa_'))
async def get_answer(callback: types.CallbackQuery):
    qa = await rq.get_qa(int(callback.data.split('_')[1]))
    await callback.message.edit_text(f'<b><i>{qa.question}</i></b>\n\n{qa.answer}', reply_markup=kb.back_to_questions)

#  Media
@router.message(or_f(Command('media'), ('наші медіа' == F.text.lower())))
async def media(message: types.Message):
    await message.answer('Список наших медіа', reply_markup=await kb.media_list())
