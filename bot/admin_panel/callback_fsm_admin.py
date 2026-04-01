from aiogram import F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from aiohttp import ClientSession

from bot.FSM import AdminConfirm

from .handlers import admin_router
from .kb.inline import ProductOrder, confirm_kb
from .order_requests import send_order, cancel_order, confirm_order


@admin_router.callback_query()
async def debug_all(callback: CallbackQuery):
    print(f"🔔 ЛЮБОЙ CALLBACK: {callback.data}")
    await callback.answer()


@admin_router.callback_query(ProductOrder.filter(F.action.in_(['send_order', 'cancel_order', 'confirm_order'])))
async def confirm_doing(callback: CallbackQuery, callback_data: ProductOrder, state: FSMContext):
    await state.set_state(AdminConfirm.waiting)
    await state.update_data(order_id = callback_data.id, action=callback_data.action, action_order=callback_data.action_order)

    await callback.message.answer(
        text='Вы уверены в своем решении?',
        reply_markup=confirm_kb,)
    await callback.answer()


@admin_router.callback_query(AdminConfirm.waiting, F.data == 'confirm')
async def confirm_yes(callback: CallbackQuery, state: FSMContext, session: ClientSession):
    data = await state.get_data()

    order_id = data.get('order_id')
    action_order = data.get('action_order')
    action = data.get('action')

    await state.set_state(AdminConfirm.waiting)

    if action == 'send_order':
        await send_order(order_id, session)
    elif action == 'cancel_order':
        await cancel_order(order_id, session)
    elif action == 'confirm_order':
        await confirm_order(order_id, session)
    
    # await callback.message.answer(r)