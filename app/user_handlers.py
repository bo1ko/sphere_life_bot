from aiogram import Router, F, types
from aiogram.filters import CommandStart, Command, or_f
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from app.utils.get_qa import get_data
import app.database.requests as rq
import app.keyboards as kb


router = Router()
data = get_data()

class City(StatesGroup):
    is_right = State()
    name = State()

class Admin(StatesGroup):
    username = State()

class Location(StatesGroup):
    name = State()
    name_ru = State()
    address = State()
    maps_url = State()


#  /start
@router.message(CommandStart())
async def cmd_start(message: types.Message):
    await rq.set_user(message.from_user.id, message.from_user.username)
    await message.answer('Ласкаво просимо до @spherelife_bot! 🤖\nТут ви зможете дізнатся всю цікаву вам інформацію.', reply_markup=kb.main)

#  Menu
@router.message(Command('menu'))
async def cmd_menu(message: types.Message):
    await message.answer('Ви перейшли в головне меню', reply_markup=kb.main)

#  Locations
@router.message(or_f(Command('locations'), ('наше місцезнаходження' == F.text.lower())))
async def get_city(message: types.Message, state: FSMContext):
    await state.set_state(City.name) # branchLocation
    await message.answer('Введіть назву вашого міста')

#  Locations / Get city
@router.message(City.name)
async def check_city(message: types.Message, state: FSMContext):
    await state.update_data(city=message.text)
    city_data = await state.get_data()
    locations = await rq.get_locations()
    
    if await rq.get_location(city_data['city'].lower()):
        str_locations = '📍 Адреси, за якими ви можете нас знайти 📍\n\n'
        count = 1
        for location in locations:
            str_locations += f'{count}. {location.address}\n👉 <a href="{location.maps_url}">Перейти до Google Maps</a>\n\n' 
            count += 1
        await message.answer(str_locations, reply_markup=kb.main)
    else:
        await rq.update_ask_city(message.from_user.id)
        await rq.set_city(city_data['city'].lower())
        
        str_locations = '😔 На жаль, наших закладів ще немає у вашому місті 🌍\nМи врахували вашу відповідь, і як тільки відкриємося у вашому місті, повідомимо вас 📩\n\nОсь адреси, за якими ви можете нас знайти в інших містах 📍\n\n'
        count = 1
        for location in locations:
            str_locations += f'{count}. {location.address}\n👉 <a href="{location.maps_url}">Перейти до Google Maps</a>\n\n' 
            count += 1
        await message.answer(str_locations, reply_markup=kb.main)

    await state.clear()

#  Questions&Answers
@router.message(or_f(Command('questions'), ('відповіді на питання' == F.text.lower())))
async def questions(message: types.Message):    
    await message.answer('<b><i>📚❓ Відповіді на популярні запитання 📚❓</i></b>', reply_markup=await kb.question_list(data))

#  Callback questions&answers
@router.callback_query(F.data.startswith('back_to_questions'))
async def questions(callback: types.CallbackQuery):    
    await callback.message.edit_text('<b><i>📚❓ Відповіді на популярні запитання 📚❓</i></b>', reply_markup=await kb.question_list(data))

@router.callback_query(F.data.startswith('qa_'))
async def get_answer(callback: types.CallbackQuery):
    await callback.message.edit_text(f'<b><i>{data[int(callback.data.split('_')[1])][0]}</i></b>\n\n{data[int(callback.data.split('_')[1])][1]}', reply_markup=kb.back_to_questions)

#  Media
@router.message(or_f(Command('our_media'), ('наші медіа' == F.text.lower())))
async def our_media(message: types.Message):
    await message.answer('Список наших медіа', reply_markup=await kb.media_list())
