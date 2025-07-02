from aiogram import Router

from app.bot.filters import BanFilter

from app.bot.handlers.other_handlers import echo_router
from app.bot.handlers.user_menu import user_router
from app.bot.handlers.region_admin import region_admin_router
from app.bot.handlers.reports import reports_router

main_router = Router()
main_router.message.filter(BanFilter())

main_router.include_routers(
    user_router, region_admin_router, reports_router, echo_router
)
