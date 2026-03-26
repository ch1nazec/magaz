"""
Файл с запросами на апи с заказами
"""

from create_bot import BOT_API, BACKEND_PORT, BACKEND_URL
from aiohttp.client import ClientSession


headers = {'X-Bot-Token': BOT_API}
main_url = f'{BACKEND_URL}:{BACKEND_PORT}/api/order/'


async def get_orders(session: ClientSession, tg_id: int, params: dict = None) -> dict:
    if params is None:
        params = {}

    url = f'{main_url}?telegram_id={tg_id}'

    for param, value_param in params.items():
        url += f'&{param}={value_param}'

    async with session.get(url, headers=headers) as response:
        return await response.json()


async def get_order(session: ClientSession, id: int) -> dict:
    url = f'{main_url}{id}/'
    async with session.get(url, headers=headers) as response:
        return await response.json()