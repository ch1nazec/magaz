from create_bot import headers, main_url_order
from aiohttp.client import ClientSession


async def get_orders(mess: str, session: ClientSession, page: int = 1) -> list[dict]:
    try:
        filter_order = {
            'active_adm': '?status=processing&status=shipped&page=3&status=new',
            'closed_adm': '?status=cancelled',
        }
        url = f'{main_url_order}{filter_order.get(mess)}&page={page}'

        async with session.get(url, headers=headers) as response:
            data = await response.json()
            return data
    except Exception as err:
        print(f'Ошибка при отправке запроса: {str(err)}')