"""
Файл с запросами на апи с заказами
"""

from create_bot import headers, main_url_order
from aiohttp.client import ClientSession


async def get_orders(session: ClientSession, tg_id: int, params: dict = None) -> dict:
    if params is None:
        params = {}

    url = f'{main_url_order}?telegram_id={tg_id}'

    for param, value_param in params.items():
        url += f'&{param}={value_param}'

    async with session.get(url, headers=headers) as response:
        return await response.json()


async def get_order(session: ClientSession, id: int) -> dict:
    url = f'{main_url_order}{id}/'
    async with session.get(url, headers=headers) as response:
        return await response.json()