from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery

from aiogram import Router, F
from aiogram.filters import Command
from aiohttp.client import ClientSession
from aiohttp import web

from kb.reply import orders_type
from kb.inline import build_btn, DictAction

from requests.order import get_orders, get_order
import textwrap

router = Router()

@router.message(Command('order'))
async def order_mess(message: Message, session: ClientSession) -> None:
    await message.answer('Выберите тип заказа', reply_markup=orders_type())


@router.message(F.text == 'Активные заказы')
async def active_order(message: Message, session: ClientSession, data: dict = None) -> None:
    if data is None:
        data = {}

    user_id = message.from_user.id
    orders_user = (await get_orders(
        session=session,
        params={'status__in': 'new,shipped,processing'},
        tg_id=user_id))
    
    orders_result = orders_user.get('results')

    if not orders_result:
        await message.reply('Активных заказов нет', reply_markup=ReplyKeyboardRemove())
    else:
        data['temp_data'] = orders_result
        for order in orders_result:

            await message.answer(
                text=f"""
            Заказ #{order.get('id')}
            Номер телефона {order.get('phone_number')}
            Адрес доставки: {order.get('address')}
            Стоимость заказа: {order.get('total_amount')}""")
        await message.answer('Выберите заказ', reply_markup=build_btn(orders_result))


@router.callback_query(DictAction.filter(F.action.contains("callback_order_")))
async def order_details(callback: CallbackQuery, callback_data: DictAction, session: ClientSession) -> None:
    data_order = await get_order(session=session, id=callback_data.order_id)
    result_string = ""

    for item in data_order.get('items'):
        temp_string = textwrap.dedent(f"""
        Название: {item.get('product')}
        Цвет: {item.get('color')}
        Размер: {item.get('size')}
        Количество: {item.get('quantity')}
        Цена: {item.get('price')} руб.
        """)
        result_string += (temp_string)
    
    await callback.message.answer(text=result_string, show_alert=False)
    await callback.answer()


async def send_order_notification(request):
    try:
        data = await request.json()
        bot = request.app['bot']

        data_json = dict(
            telegram_id=data.get('telegram_id'),
            id=data.get('id'),
            total_amount=data.get('total_amount'))

        text = textwrap.dedent(f"""
                    Заказ #{data_json.get('id')}
                    Сумма: {data_json.get('total_amount')}
                    """)
        await bot.send_message(data_json.get('telegram_id'), text, parse_mode='Markdown', reply_markup=build_btn(data_json))

        return web.Response(status=200)
    except Exception as e:
        return web.Response(status=500, text=str(e))