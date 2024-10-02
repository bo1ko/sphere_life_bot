from aiogram import types
from app.database import requests as rq

import app.keyboards.keyboards as kb

async def city_check(locations, text='📍 Адреси, за якими ви можете нас знайти 📍\n\n'):
    count = 1
    for location in locations:
        text += f'{count}. {location.address}\n👉 <a href="{location.map_url}">Перейти до Google Maps</a>\n\n'
        count += 1
    
    return text


async def get_questions():
    qa_set = await rq.get_qa_set()
    qa_list = []

    for i in qa_set:
        qa_list.append([i.id, i.question, i.answer])

    return qa_list


async def send_questions_message(target, qa_list):
    text = '<b><i>📚❓ Відповіді на популярні запитання 📚❓</i></b>'
    markup = await kb.question_list(qa_list)

    if isinstance(target, types.Message):
        await target.answer(text, reply_markup=markup)
    elif isinstance(target, types.CallbackQuery):
        await target.message.edit_text(text, reply_markup=markup)

async def choose_payment_type(api_services_data, service_index):
    varied = api_services_data[service_index]['payment'].get('varied', {}).get('defaultPrice', {}).get('value', False)
    fixed = api_services_data[service_index]['payment'].get('fixed', {}).get('price', {}).get('value', False)
    custom = api_services_data[service_index]['payment'].get('custom', {}).get('description', False)

    if varied:
        return [varied, 0]
    elif fixed:
        return [fixed, 1]
    elif custom:
        return [custom, 2]