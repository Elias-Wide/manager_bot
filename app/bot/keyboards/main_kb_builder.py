"""Модуль по созданию клавиатур в меню."""

from typing import TypeAlias

from aiogram.types import (
    BotCommand,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputMediaPhoto,
    ReplyKeyboardMarkup,
)
from aiogram import Bot
from aiogram.utils.keyboard import InlineKeyboardBuilder

# from app.bot.keyboards.banners import get_img
from app.bot.keyboards.buttons import BACK_BTN
from app.core.constants import (
    DEFAULT_KEYBOARD_SIZE,
    MAIN_MENU,
    MAIN_MENU_COMMANDS,
)
from app.bot.handlers.callbacks.menucallback import MenuCallBack
from app.core.config import settings


KeyboardMarkup: TypeAlias = InlineKeyboardMarkup | ReplyKeyboardMarkup


async def set_main_menu(bot: Bot) -> None:
    """Установить основное меню, назначить команды с описаниями."""
    main_menu_commands = [
        BotCommand(command=command, description=description)
        for command, description in MAIN_MENU_COMMANDS.items()
    ]
    await bot.set_chat_menu_button(menu_button=None)
    await bot.set_my_commands(main_menu_commands)


async def get_btns(
    *,
    menu_name: str,
    next_menu: str | None = None,
    level: int = 0,
    size: int = DEFAULT_KEYBOARD_SIZE,
    btns_data: tuple[str, str] | None = None,
    point_id: int | None = None,
    user_id: int | None = None,
    previous_menu: str = MAIN_MENU,
    need_back_btn: bool = True,
) -> list[InlineKeyboardButton]:
    """
    Создание клавиатуры.
    Текст кнопок и колбэк дата берется из констант модуля buttons.
    Если btns_data нет - создается только кнопка Назад.
    """
    kb_builder = InlineKeyboardBuilder()
    btns = []
    if btns_data:
        for menu_name, text in btns_data:
            btns.append(
                InlineKeyboardButton(
                    text=text,
                    callback_data=MenuCallBack(
                        level=level + 1,
                        menu_name=menu_name,
                        user_id=user_id,
                        point_id=point_id,
                    ).pack(),
                ),
            )
    if need_back_btn:
        btns.append(
            InlineKeyboardButton(
                text=BACK_BTN,
                callback_data=MenuCallBack(
                    user_id=user_id,
                    level=level - 1,
                    point_id=point_id,
                    menu_name=previous_menu,
                ).pack(),
            )
        )
    kb_builder.row(*btns, width=size)
    return kb_builder.as_markup()
