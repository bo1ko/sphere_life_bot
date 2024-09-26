from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

user_main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Список послуг')],
    [KeyboardButton(text='Наше місцезнаходження')],
    [KeyboardButton(text='Відповіді на питання')],
    [KeyboardButton(text='Наші медіа')],
],
resize_keyboard=True, input_field_placeholder='Виберіть пункт меню...')

admin_main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Редагувати "Наші медіа"')],
    [KeyboardButton(text='Вийти з адмінки')],
],
resize_keyboard=True, input_field_placeholder='Виберіть пункт меню...')

