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