from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def admin_order_check():
    buttons = [
        [KeyboardButton(text='Активные заказы адм')],
        [KeyboardButton(text='Закрытые заказы адм')],
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)