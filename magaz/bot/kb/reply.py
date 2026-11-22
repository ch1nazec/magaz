from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def orders_type():
    buttons = [
        [KeyboardButton(text='active_adm',)],
        [KeyboardButton(text='closed_adm',)],
    ]
    
    return ReplyKeyboardMarkup(keyboard=buttons,
                               resize_keyboard=True,
                               one_time_keyboard=True)