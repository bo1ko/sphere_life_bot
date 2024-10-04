from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from datetime import datetime

import locale

from app.utils.wix_api import api_services_data


locale.setlocale(locale.LC_ALL, 'uk_UA.UTF-8')

async def choose_location(service_id):
    keyboard = InlineKeyboardBuilder()

    for location in api_services_data[service_id]['locations']:
        keyboard.add(InlineKeyboardButton(text=location['business']['name'], callback_data=f'location_service_{location["id"]}'))

    return keyboard.adjust(1).as_markup()

async def choose_date(api_availability_data):
    keyboard = InlineKeyboardBuilder()
    day_list = []

    for date in api_availability_data:
        date_name = datetime.fromisoformat(date['startDate'].replace("Z", "+00:00"))

        if date_name.day in day_list:
            continue

        day_list.append(date_name.day)
        keyboard.add(InlineKeyboardButton(text=f'{date_name.strftime("%d.%m")}', callback_data=f'day_{date["startDate"]}'))

    return keyboard.adjust(5).as_markup()

async def choose_time(start_date, api_availability_data):
    keyboard = InlineKeyboardBuilder()

    for day in api_availability_data:
        start_time = datetime.fromisoformat(day['startDate'].replace("Z", "+00:00"))
        end_time = datetime.fromisoformat(day['endDate'].replace("Z", "+00:00"))
        time_range_str = f"{start_time.strftime('%H:%M')}-{end_time.strftime('%H:%M')}"

        if start_date in day['startDate']:
            keyboard.add(InlineKeyboardButton(text=f'{time_range_str}', callback_data=f'hour_{day["startDate"]}'))

    return keyboard.adjust(2).as_markup()

async def is_soldier():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text='Так', callback_data=f'is_soldier_yes'))
    keyboard.add(InlineKeyboardButton(text='Ні', callback_data=f'is_soldier_no'))

    return keyboard.adjust(1).as_markup()

async def price_agree():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text='Погоджуюсь', callback_data='price_agree'))

    return keyboard.adjust(1).as_markup()
