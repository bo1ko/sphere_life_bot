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
    name = State()


#  /start
@router.message(CommandStart())
async def cmd_start(message: types.Message):
    await rq.set_user(message.from_user.id, message.from_user.username)
    await message.answer('Ласкаво просимо до @spherelife_bot! 🤖\nТут ви зможете дізнатся всю цікаву вам інформацію.', reply_markup=kb.main)

#  Menu
@router.message(Command('menu'))
async def cmd_menu(message: types.Message):
    await message.answer('Ви перейшли в головне меню', reply_markup=kb.main)

@router.message(or_f(Command('locations'), ('наше місцезнаходження' == F.text.lower())))
async def get_city(message: types.Message, state: FSMContext):
    await state.set_state(City.name) # branchLocation
    await message.answer('Введіть назву вашого міста')

@router.message(City.name)
async def check_city(message: types.Message, state: FSMContext):
    await state.update_data(city=message.text)
    city_data = await state.get_data()
    await rq.set_city(city_data['city'].lower())
    
    await message.answer(f'Your city name {city_data['city']}')

#  Questions&Answers
@router.message(or_f(Command('questions'), ('відповіді на питання' == F.text.lower())))
async def questions(message: types.Message):    
    await message.answer('<b><i>📚❓ Відповіді на популярні запитання 📚❓</i></b>', reply_markup=await kb.question_list(data))

@router.callback_query(F.data.startswith('qa_'))
async def get_answer(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.answer(f'<b><i>{data[int(callback.data.split('_')[1])][0]}</i></b>\n\n{data[int(callback.data.split('_')[1])][1]}')

#  Media
@router.message(or_f(Command('our_media'), ('наші медіа' == F.text.lower())))
async def our_media(message: types.Message):
    await message.answer('Список наших медіа', reply_markup=await kb.media_list())
