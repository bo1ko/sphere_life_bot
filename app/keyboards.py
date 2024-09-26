from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.database.requests import get_media

main = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='Список послуг')],
        [KeyboardButton(text='Наше місцезнаходження')],
        [KeyboardButton(text='Відповіді на питання')],
        [KeyboardButton(text='Наші медіа')],
    ], resize_keyboard=True, input_field_placeholder='Виберіть пункт меню...'
)

async def media():
    all_media = await get_media()
    keyboard = InlineKeyboardBuilder()

    for media in all_media:
        keyboard.add(InlineKeyboardButton(text=media.media_name, url=media.media_link))

    return keyboard.adjust(2).as_markup()
