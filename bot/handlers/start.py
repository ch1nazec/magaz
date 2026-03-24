from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message


router = Router()

@router.message(CommandStart())
async def command_start_handler(mess: Message):
    await mess.answer('Ну здарова, квакозябра!')


# @router.message()
# async def echo_handler(mess: Message):
#     await mess.answer(f'Ты только что сказал: {mess.text}!')