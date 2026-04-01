from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from decouple import config

from redis.asyncio import Redis
from aiogram.fsm.storage.redis import RedisStorage


BOT_API = config('BOT_API')
HOST = config('HOST')
PORT = int(config('PORT'))
BASE_URL = config('BASE_URL')
WEBHOOK_APP = f'/{BOT_API}'
ADMIN = config('ADMIN_ID')

BACKEND_URL = config('BACKEND_URL')
BACKEND_PORT = config('BACKEND_PORT')

REDIS_HOST = config('REDIS_HOST')
REDIS_PORT = config('REDIS_PORT')

headers = {'X-Bot-Token': BOT_API}
main_url = f'{BACKEND_URL}:{BACKEND_PORT}'
main_url_order = f'{main_url}/api/order/'



bot = Bot(token=BOT_API, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()