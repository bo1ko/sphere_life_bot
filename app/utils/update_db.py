from app.database.requests import clear_tables, add_media, add_location, add_qa
from app.utils.excel_data import get_excel_data
from aiogram import types

import app.keyboards.keyboards as kb


async def update_data(target: types.Message):
    try:
        await target.answer('Розпочинаю оновлення даних...')
        data = get_excel_data()

        await clear_tables()

        for i in data['media']:
            await add_media(i[0], i[1])

        await target.answer('Медіа успішно оновлені ✔')

        for i in data['locations']:
            await add_location(i[0].lower(), i[1].lower(), i[2], i[3])

        await target.answer('Локації успішно оновлені ✔')

        for i in data['qa']:
            await add_qa(i[0], i[1])

        await target.answer('Відповіді на запитання успішно оновлені ✔')

        await target.answer('Усі таблиці були успішно оновлені ✅', reply_markup=kb.main)
    except Exception as e:
        await target.answer(f'❌ Помилка при оновленні таблиць ❌\n\n{e}')
