from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters.callback_data import CallbackData


class ProductId(CallbackData, prefix="pr_id"):
    id: int
    action: str
    action_order: str


class Pagination(CallbackData, prefix="pag"):
    page: int
    action: str


def admin_order_builder(data: list[dict], action: str, page: int = 1) -> InlineKeyboardMarkup:
    action_callback = {
        'Активные заказы (адм).': 'active',
        'Закрытые заказы (адм).': 'closed',}
    inline_builder = InlineKeyboardBuilder()

    for order in data.get('results'):
        order_id = order.get('id')

        inline_builder.add(InlineKeyboardButton(
            text=f'Заказ #{order_id}',
            callback_data=ProductId(action=(f'callback_detail_order'),
                                    id=order_id, action_order=action)))
    
    inline_builder.adjust(1)

    nav_buttons = []

    if data.get('previous'):
        nav_buttons.append(
            InlineKeyboardButton(
                text='⬅',
                callback_data=Pagination(page=page - 1, action=action).pack()))
    
    if data.get('next'):
        nav_buttons.append(
            InlineKeyboardButton(
                text='➡',
                callback_data=Pagination(page=page + 1, action=action).pack()))
    
    if nav_buttons:
        inline_builder.add(*nav_buttons)
    return inline_builder.as_markup()



def admin_cancel_order(id: int, action: str, action_order: str) -> InlineKeyboardMarkup:
    admin_cancel_order_inline = InlineKeyboardMarkup(
        [InlineKeyboardButton(text='Подробнее', callback_data=ProductId(id=id,
                                                                        action=action,
                                                                        action_order=action_order).pack())])