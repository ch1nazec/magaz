from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from .list_admin import ADMIN_LIST 
from .kb.inline import admin_order_builder

from aiohttp import ClientSession

# from kb.reply import admin_order_check
from .order_requests import get_orders

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

def admin_order_check():
    buttons = [
        [KeyboardButton(text='Активные заказы (адм).')],
        [KeyboardButton(text='Закрытые заказы (адм).')],
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)


admin_router = Router()
admin_router.message.filter(F.from_user.id.in_(ADMIN_LIST))


@admin_router.message(Command('admin-start'))
async def admin_start(message: Message, session: ClientSession):
    await message.answer(
        'Выберите действие',
        reply_markup=admin_order_check())


@admin_router.message(F.text == 'Активные заказы (адм).')
async def active_orders(message: Message, session: ClientSession):
    data_orders = await get_orders(mess=message.text, session=session)

    if data_orders:
        await message.reply(
            text="Выберите один из заказов снизу",
            reply_markup=admin_order_builder(data_orders, message.text))


@admin_router.message(F.text == 'Закрытые заказы (адм).')
async def active_orders(message: Message, session: ClientSession):
    data_orders = await get_orders(mess=message.text, session=session)

    if data_orders:
        await message.reply(
            text="Выберите один из закрытых заказов снизу",
            reply_markup=admin_order_builder(data_orders, message.text))