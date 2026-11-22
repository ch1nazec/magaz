from aiohttp.client import ClientSession
from create_bot import tg_bunch, headers


async def bunch_telegram(id: int, session: ClientSession) -> dict:
    async with session.post(f'{tg_bunch}{id}', headers=headers) as response:
        data = await response.json()

        if response.ok:
            return data
        else:
            raise Exception(f'Ошибка в привязке аккаунта: {data}')
    