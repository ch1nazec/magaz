from aiogram.types import Message
from aiogram import Router, Dispatcher
from aiogram.filters import Command
from create_bot import BACKEND_URL, BACKEND_PORT
import aiohttp



router = Router()

async def get_orders(session):
    url = f'{BACKEND_URL}:{BACKEND_PORT}/api/productvariants/'

    async with session.get(url) as response:
        return await response.json()


@router.message()
async def catch_all(message: Message, session):
    data = await get_orders(session)
    for item in data:
        text = f"""{item['product']['name']} - {item['product']['category']}"""
        await message.answer(text)