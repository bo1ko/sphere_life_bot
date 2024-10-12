from aiogram import BaseMiddleware
from aiogram.types import Message
from aiogram.dispatcher.flags import get_flag

import app.database.requests as rq

class AdminCheckMiddleware(BaseMiddleware):

    async def __call__(self, handler, event: Message, data: dict):
        admin_required = get_flag(data, 'admin_required', default=False)

        telegram_id = event.from_user.id
        username = event.from_user.username

        user = await rq.get_user(telegram_id)
            
        if not user:
            user = await rq.set_user(telegram_id, username)
        
        if admin_required and user:
            if not user.is_admin:
                return

        return await handler(event, data)
