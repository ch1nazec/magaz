from aiogram.fsm.state import StatesGroup, State


class AdminConfirm(StatesGroup):
    waiting = State()