from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.database.requests import get_media, get_services, get_service
from app.utils.wix_api import api_services_data


main = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='Список процедур')],
        [KeyboardButton(text='Наше місцезнаходження')],
        [KeyboardButton(text='Відповіді на питання')],
        [KeyboardButton(text='Наші медіа')],
    ], resize_keyboard=True, input_field_placeholder='Виберіть пункт меню...'
)

subscribe = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='🔥 Підписатися 🔥', url='https://t.me/spherelife')],
        [InlineKeyboardButton(text='Я вже підписався!', callback_data='continue')],
        [InlineKeyboardButton(text='Нецікаво', callback_data='continue')]
    ]
)

back_to_questions = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Назад до питань', callback_data='back_to_questions')]
    ]
)

async def back_to_service_info(service_index: int):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text='Назад', callback_data=f'service_{service_index}'))

    return keyboard.adjust(1).as_markup()
async def service_list():
    keyboard = InlineKeyboardBuilder()
    count = 0

    for service in api_services_data:
        keyboard.add(InlineKeyboardButton(text=service['name'], callback_data=f'service_{count}'))
        count += 1

    return keyboard.adjust(1).as_markup()

async def service_info(service_index: int):
    keyboard = InlineKeyboardBuilder()

    keyboard.add(InlineKeyboardButton(text='Записатися', callback_data=f'register_service_{service_index}'))
    keyboard.add(InlineKeyboardButton(text='Детальніше', callback_data=f'more_info_{service_index}'))
    keyboard.add(InlineKeyboardButton(text='Назад', callback_data='back_to_service_list'))

    return keyboard.adjust(1, 2).as_markup()

async def media_list():
    all_media = await get_media()
    keyboard = InlineKeyboardBuilder()

    for media in all_media:
        keyboard.add(InlineKeyboardButton(text=media.media_name, url=media.media_link))

    return keyboard.adjust(2).as_markup()

async def question_list(data: list):
    keyboard = InlineKeyboardBuilder()

    for i in data:
        keyboard.add(InlineKeyboardButton(text=i[1], callback_data=f'qa_{i[0]}'))

    return keyboard.adjust(1).as_markup()
