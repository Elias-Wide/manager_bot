from contextlib import asynccontextmanager

from aiogram.types import Update
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI, Request
from sqladmin import Admin

from app.admin.adminview import admin_views
from app.admin.auth import authentication_backend
from app.bot.handlers.registration import registration_router
from app.bot.init_bot import bot, dp, start_bot, stop_bot
from app.bot.keyboards.main_kb_builder import set_main_menu
from app.bot.routers import main_router
from app.bot.scheduler import (
    delete_old_workdays,
    delete_reports_photo,
    notify_region_admins_about_missing_reports,
)
from app.core.config import settings
from app.core.database import engine
from app.core.logging import get_logger

logger = get_logger(__name__)

WEBHOOK_PATH = f"/bot/{settings.telegram.bot_token.get_secret_value()}"
WEBHOOK_URL = f"{settings.telegram.webhook_host}/webhook"


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting bot setup...")
    scheduler = AsyncIOScheduler()
    scheduler.start()
    scheduler.add_job(
        notify_region_admins_about_missing_reports,
        kwargs={"working_schedule": "lower"},
        trigger="cron",
        hour=settings.telegram.reports_time_lower,
    )
    scheduler.add_job(
        notify_region_admins_about_missing_reports,
        kwargs={"working_schedule": "middle"},
        trigger="cron",
        hour=settings.telegram.reports_time_middle,
    )
    scheduler.add_job(
        delete_reports_photo,
        trigger="cron",
        day=1,
        hour=1,
        minute=0,
    )
    scheduler.add_job(delete_old_workdays, trigger="cron", day=1, hour=3)
    await start_bot()
    await bot.set_webhook(
        url=WEBHOOK_URL,
        allowed_updates=dp.resolve_used_update_types(),
        drop_pending_updates=True,
    )
    await set_main_menu(bot)
    dp.include_router(main_router)
    dp.include_router(registration_router)
    # dp.include_router(admin_router)
    yield
    logger.info("Shutting down bot...")
    await bot.delete_webhook()
    await stop_bot()


app = FastAPI(lifespan=lifespan)


@app.post("/webhook")
async def webhook(request: Request) -> None:
    update = Update.model_validate(await request.json(), context={"bot": bot})
    await dp.feed_update(bot, update)


admin = Admin(
    app=app,
    engine=engine,
    authentication_backend=authentication_backend,
)

for view in admin_views:
    admin.add_view(view)
