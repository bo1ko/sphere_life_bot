from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Список послуг')],
    [KeyboardButton(text='Наше місцезнаходження')],
    [KeyboardButton(text='Відповіді на питання')],
    [KeyboardButton(text='Наші медіа')],
],
resize_keyboard=True, input_field_placeholder='Виберіть пункт меню...')