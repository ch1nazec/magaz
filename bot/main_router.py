from admin_panel.handlers import admin_router
from admin_panel.callback_admin import router_admin_call
from handlers.start import router as start_router
from handlers.orders import router as order_router

all_routers = [start_router, admin_router, order_router, router_admin_call]