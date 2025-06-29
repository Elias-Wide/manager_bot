from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message


from app.bot.handlers.callbacks.main_menu import (
    procces_main_menu_comand,
)
from app.bot.keyboards.buttons import MAIN_MENU_PAGES
from app.bot.keyboards.main_kb_builder import MenuCallBack


user_router = Router()


@user_router.message(CommandStart())
async def process_start_command(
    message: Message,
    state: FSMContext,
) -> None:
    """После завершения анкетирования. Начало самого бота."""
    await procces_main_menu_comand(message)
    await state.clear()
