from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from decouple import config


BOT_API = config('BOT_API')
HOST = config('HOST')
PORT = int(config('PORT'))
BASE_URL = config('BASE_URL')
WEBHOOK_APP = f'/{BOT_API}'
ADMIN = config('ADMIN_ID')

BACKEND_URL = config('BACKEND_URL')
BACKEND_PORT = config('BACKEND_PORT')


bot = Bot(token=BOT_API, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()