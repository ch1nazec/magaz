from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

from dataclasses import dataclass, field


class ProductId(CallbackData, prefix="pr_id"):
    id: int
    action: str
    action_order: str


class Pagination(CallbackData, prefix="pag"):
    page: int
    action: str


class ProductOrder(CallbackData, prefix="product_detail"):
    id: int
    action: str
    action_order: str
    


@dataclass
class OrderKeyboard:
    id: int
    action_order: str
    _keyboard: list = field(default_factory=list)

    def detail_order(self):
        self._keyboard.append([InlineKeyboardButton(text='Подробнее', callback_data=ProductOrder(action='detail_order',
                                                                                                 id=self.id,
                                                                                                 action_order=self.action_order).pack())])
        return self
    
    def order_status(self):
        self._keyboard.append(
            [
                InlineKeyboardButton(text='Отправить заказ', callback_data=ProductOrder(id=self.id, action='send_order', action_order=self.action_order).pack()),
                InlineKeyboardButton(text='Отменить заказ', callback_data=ProductOrder(id=self.id, action='cancel_order', action_order=self.action_order).pack()),
            ]
        )
        return self
    
    def order_confirm(self):
        self._keyboard.append(
            [InlineKeyboardButton(text='Закрыть заказ', callback_data=ProductOrder(id=self.id, action='confirm_order', action_order=self.action_order).pack())]
        )
        return self
    
    def back(self):
        self._keyboard.append(
            [InlineKeyboardButton(text='НАЗАД', callback_data=ProductOrder(id=self.id, action='back_order', action_order=self.action_order).pack())]
        )
        return self
    
    def build(self):
        return InlineKeyboardMarkup(inline_keyboard=self._keyboard)


def admin_order_builder(data: list[dict], action: str, page: int = 1) -> InlineKeyboardMarkup:
    inline_builder = InlineKeyboardBuilder()

    orders = data.get('results') if isinstance(data, dict) else data
    for order in orders:
        order_id = order.get('id')
        product_data = ProductOrder(action=(f'cb_det_order'),
                                    id=order_id, action_order=action).pack()

        inline_builder.add(InlineKeyboardButton(
            text=f'Заказ #{order_id}',
            callback_data=product_data))
    
    inline_builder.adjust(1)

    nav_buttons = []

    if isinstance(data, dict) and data.get('previous'):
        page_prev = page - 1 if page - 1 > 0 else page

        prev = Pagination(page=page_prev, action=action).pack()
        nav_buttons.append(
            InlineKeyboardButton(
                text='⬅',
                callback_data=prev))
    
    if isinstance(data, dict) and data.get('next'):
        next = Pagination(page=page + 1, action=action).pack()
        nav_buttons.append(
            InlineKeyboardButton(
                text='➡',
                callback_data=next))
    
    if nav_buttons:
        inline_builder.row(*nav_buttons)
    return inline_builder.as_markup()



def admin_cancel_order(id: int, action: str, action_order: str) -> InlineKeyboardMarkup:
    product_data = ProductId(id=id, action=action, action_order=action_order).pack()
    return InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Подробнее', callback_data=product_data)]])


def get_order_kb(order_id: int, action: str, closed: False) -> InlineKeyboardMarkup:
    order_kb = OrderKeyboard(id=order_id, action_order=action)

    if not closed:
        return (order_kb.detail_order()
            .order_status()
            .order_confirm()
            .back()
            .build())
    else:
        return (order_kb.detail_order()
                .back())


"""Кнопки назад по разным целям"""
def back_to_detail_order(id: int, action_order: str) -> InlineKeyboardMarkup:
    """Функция с возвратом обратно в меню взаимодействия с заказом из кнопки подробнее"""
    product = ProductOrder(id=id, action='back_to_menu', action_order=action_order)
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Назад в меню', callback_data=product.pack())]])