from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from kb.inline import link_start_button

from aiohttp import ClientSession


router = Router()

@router.message(CommandStart())
async def command_start_handler(mess: Message):
    start_inline = link_start_button(mess.from_user.id)
    await mess.answer('Привет! для привязки аккаунта нажми на кнопку ниже', reply_markup=start_inline)



# @router.message()
# async def echo_handler(mess: Message):
#     await mess.answer(f'Ты только что сказал: {mess.text}!')