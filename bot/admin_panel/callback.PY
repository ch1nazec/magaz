from handlers import admin_router
from kb.inline import Pagination, admin_order_builder, ProductId
from .order_requests import get_orders
from ..requests.order import get_order

from aiogram.types import CallbackQuery
from aiogram import F

import textwrap

from aiohttp import ClientSession


@admin_router.callback_query(Pagination.filter())
async def pagination_orders(callback: CallbackQuery, session: ClientSession, callback_data: Pagination):
    data_orders = await get_orders(
        mess=callback_data.action,
        session=session,
        page=callback_data.page)
    
    await callback.message.edit_reply_markup(
        reply_markup=admin_order_builder(data_orders,
                                         callback_data.action,
                                         page=callback_data.page))


@admin_router.callback_query(ProductId.filter(F.text == 'callback_detail_order'))
async def product_closed_detail(callback: CallbackQuery, session: ClientSession, callback_data: ProductId):
    order_data = await get_order(session=session, id=callback_data.id)
    if not order_data:
        await callback.message.answer('Заказа в базе данных нет.')
        await callback.message()
    
    message_text = '' 
    message_text += textwrap(
    f"""
    Заказ #{order_data.get('id')}
    Статус: {order_data.get("status")}
    
    Номер телефона: {order_data.get('phone_number')}
    Фамилия: {order_data.get('last_name')}
    Имя: {order_data.get('first_name')}

    Комментарий к заказу: {order_data.get('comment')}
    Адрес доставки: {order_data.get('address')}

    Дата создания заказа: {order_data.get('created_at')}
    """
    )
    await callback.message.answer(
        text=message_text)
