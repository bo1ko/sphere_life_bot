from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.database.requests import get_media


main = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='Список послуг')],
        [KeyboardButton(text='Наше місцезнаходження')],
        [KeyboardButton(text='Відповіді на питання')],
        [KeyboardButton(text='Наші медіа')],
    ], resize_keyboard=True, input_field_placeholder='Виберіть пункт меню...'
)

back_to_questions = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Назад до питань', callback_data='back_to_questions')]
    ]
)

async def media_list():
    all_media = await get_media()
    keyboard = InlineKeyboardBuilder()

    for media in all_media:
        keyboard.add(InlineKeyboardButton(text=media.media_name, url=media.media_link))

    return keyboard.adjust(2).as_markup()

async def question_list(data):
    keyboard = InlineKeyboardBuilder()
    count = 0

    for i in data:
        keyboard.add(InlineKeyboardButton(text=i[0], callback_data=f'qa_{count}'))
        count += 1
    
    return keyboard.adjust(1).as_markup()


async def answer():
    ...