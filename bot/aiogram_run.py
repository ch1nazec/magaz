import logging
from aiogram.types import BotCommand, BotCommandScopeDefault
from aiohttp import web, ClientSession
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from create_bot import bot, dp, BASE_URL, HOST, PORT, WEBHOOK_APP, ADMIN
# from handlers.main import main_router
from middleware.session_middleware import SessionMiddleware
from handlers.orders import send_order_notification

from admin_panel.handlers import admin_router
from handlers.orders import router as orders_router
from handlers.start import router as start_router

async def set_commands():
    commands = [BotCommand(command='start', description='Старт')]
    await bot.set_my_commands(commands, BotCommandScopeDefault())


async def on_startup():
    """Включить бота"""

    await set_commands()
    await bot.set_webhook(f"{BASE_URL}{WEBHOOK_APP}")
    await bot.send_message(chat_id=ADMIN, text='Бот запущен')

    session = ClientSession()
    dp.update.middleware(SessionMiddleware(session))


async def on_shutdown() -> None:
    # Отправляем сообщение администратору о том, что бот был остановлен
    await bot.send_message(chat_id=ADMIN, text='Бот остановлен!')
    # Удаляем вебхук и, при необходимости, очищаем ожидающие обновления
    await bot.delete_webhook(drop_pending_updates=True)
    # Закрываем сессию бота, освобождая ресурсы
    await bot.session.close()


def main():
    dp.include_routers(orders_router, start_router, admin_router)
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    # Создаём веб-приложение на aiohttp и настраиваем вебхук - закидываем туда диспетчера да бота
    app = web.Application()
    app['bot'] = bot
    
    app.router.add_post('/send_order', send_order_notification)

    webhook_request_handler = SimpleRequestHandler(
        dispatcher=dp, bot=bot)

    # регаем обработчик событий на опр. путь
    webhook_request_handler.register(app, path=WEBHOOK_APP)
    setup_application(app, dp, bot=bot)

    # Запуск веб-серва на опр. url
    web.run_app(app=app, host=HOST, port=PORT)


# Начала программы
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
    main()