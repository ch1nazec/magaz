# handlers/main.py
from aiogram import Router
from .start import router as start_router
from .orders import router as order_router

main_router = Router()
main_router.include_routers(start_router, order_router)