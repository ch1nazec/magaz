from create_bot import headers, main_url_order
from aiohttp.client import ClientSession


async def get_orders(mess: str, session: ClientSession, page: int = 1) -> list[dict]:
    filter_order = {
        'Активные заказы (адм).': '?status=new&?status=processing&?status=shipped',
        'Закрытые заказы (адм).': '?status=cancelled',
    }
    url = f'{main_url_order}{filter_order.get(mess)}&page={page}'

    async with session.get(url, headers=headers) as response:
        return await response.json()