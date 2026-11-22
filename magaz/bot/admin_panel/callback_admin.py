import textwrap
from datetime import datetime

from aiogram import F, Router
from aiogram.types import CallbackQuery, InlineKeyboardMarkup
from admin_panel.kb.inline import (back_to_detail_order,
                                   get_order_kb, admin_order_builder,
                                   ProductOrder,
                                   Pagination)
from requests.order import get_order
from .order_requests import get_orders

from aiohttp import ClientSession
from dataclasses import dataclass


router_admin_call = Router()

@dataclass
class MenuOrder:
    text: str
    keyboard: InlineKeyboardMarkup

def menu_order(data: dict, action: str) -> MenuOrder:
    status = data.get('status')

    last_first_name = f"{data.get('last_name')} {data.get('first_name')}"
    order_id = data.get('id')

    status_bool = True if status in ['Отменён', 'Доставлен'] else False

    text = textwrap.dedent(f"""
        Заказ #{order_id}
        Статус заказа: {data.get('status')}
        Создан: <b>{(datetime.fromisoformat(data.get('created_at'))).strftime('%d.%m.%Y')}</b>

        Фамилия Имя заказчика: {last_first_name}
        Номер телефона заказчика: {data.get('phone_number')}
        Адрес доставки: {data.get('address')}

        Комментарий к заказу: {data.get('comment')}

        Выберите действие
        """)
    return MenuOrder(text, get_order_kb(order_id=order_id,
                                        action=action,
                                        closed=status_bool))


@router_admin_call.callback_query(ProductOrder.filter(F.action.in_('cb_det_order')))
async def order_doing_call(callback: CallbackQuery, callback_data: ProductOrder, session: ClientSession):
    order_data = await get_order(session=session, id=callback_data.id)
    menu_kb = menu_order(order_data, action=callback_data.action_order)
    await callback.message.edit_text(menu_kb.text, reply_markup=menu_kb.keyboard)


@router_admin_call.callback_query(ProductOrder.filter(F.action.in_(['back_order'])))
async def back_to_orders(callback: CallbackQuery, callback_data: ProductOrder, session: ClientSession):
    await callback.message.delete()

    data_orders = await get_orders(mess=callback_data.action_order, session=session)
    text = ''
    if callback_data.action_order == 'active_adm':
        text = 'Выберите один из заказов снизу'
    else:
        text = 'Выберите один из закрытых заказов снизу'

    if data_orders:
        await callback.message.answer(
            text=text,
            reply_markup=admin_order_builder(data=data_orders, action=callback_data.action_order))


@router_admin_call.callback_query(ProductOrder.filter(F.action == 'detail_order'))
async def order_item_detail_call(callback: CallbackQuery, callback_data: ProductOrder, session: ClientSession):
    data_order = await get_order(
        session=session,
        id=callback_data.id)
    text = ""
    for item in data_order.get('items'):
        text_item = textwrap.dedent(
            f"""
            Название: {item.get('product')}
            Цвет: {item.get('color')}
            Размер: {item.get('size')}
            Количество: {item.get('quantity')}

            Итоговая стоимость за товар: {item.get('price')}\n
            """)
        text += text_item
    
    await callback.message.edit_text(text=text, reply_markup=back_to_detail_order(id=callback_data.id, action_order=callback_data.action_order))


@router_admin_call.callback_query(ProductOrder.filter(F.action == 'back_to_menu'))
async def order_back_to_menu_call(callback: CallbackQuery, callback_data: ProductOrder, session: ClientSession):

    order_data = await get_order(session=session, id=callback_data.id)
    menu_kb = menu_order(order_data, action=callback_data.action_order)

    await callback.message.edit_text(menu_kb.text, reply_markup=menu_kb.keyboard)


@router_admin_call.callback_query(Pagination.filter())
async def pagination_next_call(callback: CallbackQuery, callback_data: Pagination, session: ClientSession):
    page = callback_data.page; action = callback_data.action
    data_orders = await get_orders(mess=action,
                                   session=session, page=page)
    

    await callback.message.edit_reply_markup(
        reply_markup=admin_order_builder(data=data_orders, action=action, page=page))