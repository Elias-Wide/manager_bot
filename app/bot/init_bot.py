import os
import subprocess
 
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from app.core.config import settings
from app.points.dao import PointsDAO

bot = Bot(
    token=settings.telegram.bot_token.get_secret_value(),
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)
dp = Dispatcher()


async def start_bot():
    """
    Sends a message to the admin when the bot starts.

    This function notifies the admin that the bot has been successfully launched.
    """
    try:
        # subprocess.run(["alembic", "upgrade", "head"], capture_output=True, text=True)
        await bot.send_message(settings.telegram.admin_id, "I am running 🥳.")
        await PointsDAO.ensure_default_point()
    except:
        print("MESSAGE NOT SENT")


async def stop_bot():
    """
    Sends a message to the admin when the bot stops.

    This function notifies the admin that the bot has been stopped.
    """
    try:
        
        await bot.send_message(settings.telegram.admin_id, "The bot has been stopped.")
    except:
        pass


async def critical_message_to_admin(message: str):
    """
    Sends a critical message to the admin.

    Args:
        message (str): The critical message to be sent to the admin.
    """
    try:
        await bot.send_message(settings.telegram.admin_id, message)
    except:
        pass
