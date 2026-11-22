from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

from create_bot import tg_bunch


class DictAction(CallbackData, prefix='callback_order_'):
    action: str
    order_id: int


def link_start_button(tg_id: int) -> InlineKeyboardMarkup:
    button = InlineKeyboardButton(text='Привязать аккаунт', url=f'{tg_bunch}{tg_id}')
    return InlineKeyboardMarkup(inline_keyboard=[[button]])


def build_btn(data: list[dict]) -> InlineKeyboardMarkup:
    if isinstance(data, dict):
        data = [data]
        
    builder = InlineKeyboardBuilder()

    for item in data:
        builder.add(InlineKeyboardButton(
            text=f'Заказ #{item.get("id")}',
            callback_data=DictAction(action=f'callback_order_{item.get("id")}', order_id=item.get('id')).pack()))
    
    builder.adjust(1)
    return builder.as_markup()