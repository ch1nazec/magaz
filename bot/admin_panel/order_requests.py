from create_bot import headers, main_url_order, main_url
from aiohttp.client import ClientSession
import aiohttp

from typing import Any, Callable, Awaitable
from functools import wraps


def try_request(func: Callable[..., Awaitable[Any]]) -> Callable[..., Awaitable[Any]]:
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except aiohttp.ClientError as err:
            print(f'Сетевая ошибка в {func.__name__}: {err}')
            return {'error': str(err)}
        
        except Exception as err:
            print(f'Ошибка в {func.__name__}: {err}')
            return {'error': str(err)}
    return wrapper     


@try_request
async def get_orders(mess: str, session: ClientSession, page: int = 1) -> list[dict]:
    filter_order = {
        'active_adm': '?status=processing&status=shipped&page=3&status=new',
        'closed_adm': '?status=cancelled&status=delivered',
    }
    url = f'{main_url_order}{filter_order.get(mess)}&page={page}'

    async with session.get(url, headers=headers) as response:
        return await response.json()


@try_request
async def send_order(order_id: int, session: ClientSession):
    url = f'{main_url}/sent/{order_id}/'

    async with session.patch(url, headers=headers) as response:
        return await response.json()


@try_request
async def cancel_order(order_id: int, session: ClientSession):
    url = f'{main_url}/cancel/{order_id}/'

    async with session.patch(url, headers=headers) as response:
        return await response.json()


@try_request
async def confirm_order(order_id: int, session: ClientSession):
    url = f'{main_url}/cancel/{order_id}/'

    async with session.patch(url, headers=headers) as response:
        return await response.json()