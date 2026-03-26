from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def orders_type():
    buttons = [
        [KeyboardButton(text='Активные заказы',)],
        [KeyboardButton(text='Закрытые заказы',)],
    ]
    
    return ReplyKeyboardMarkup(keyboard=buttons,
                               resize_keyboard=True,
                               one_time_keyboard=True)