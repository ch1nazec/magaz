from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from typing import Callable, Dict, Any, Awaitable
from aiohttp import ClientSession


class SessionMiddleware(BaseMiddleware):
    def __init__(self, session: ClientSession):
        super().__init__()
        self.session = session
        
    async def __call__(self, handler, event, data):
        data['session'] = self.session
        return await handler(event, data)