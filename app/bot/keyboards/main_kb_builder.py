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

from app.bot.keyboards.banners import get_img
from app.core.constants import DEFAULT_KEYBOARD_SIZE

from app.bot.handlers.callbacks.menucallback import MenuCallBack, RegionAdminCallBack
from app.bot.keyboards.buttons import BACK_BTN, MAIN_MENU, MAIN_MENU_COMMANDS
from app.core.config import settings


KeyboardMarkup: TypeAlias = InlineKeyboardMarkup | ReplyKeyboardMarkup


async def set_main_menu(bot: Bot) -> None:
    """Set the main menu and assign commands with descriptions."""
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
    user_id: int | None = None,
    region_id: int | None = None,
    previous_menu: str = MAIN_MENU,
    need_back_btn: bool = True,
    callback_class: MenuCallBack | RegionAdminCallBack = MenuCallBack,
) -> list[InlineKeyboardButton]:
    """
    Create a keyboard.
    The button text and callback data are taken from the buttons module constants.
    If btns_data is not provided, only the Back button is created.
    """
    print(f"{btns_data=}")
    kb_builder = InlineKeyboardBuilder()
    btns = []
    if btns_data:
        for menu_name, text in btns_data:
            btns.append(
                InlineKeyboardButton(
                    text=text,
                    callback_data=callback_class(
                        level=level + 1,
                        menu_name=menu_name,
                        user_id=user_id,
                        region_id=region_id,
                    ).pack(),
                ),
            )
    if need_back_btn:
        btns.append(
            InlineKeyboardButton(
                text=BACK_BTN,
                callback_data=callback_class(
                    user_id=user_id,
                    region_id=region_id,
                    level=level,
                    menu_name=previous_menu,
                ).pack(),
            )
        )
    kb_builder.row(*btns, width=size)
    return kb_builder.as_markup()


async def get_image_and_kb(
    menu_name: str,
    user_id: int,
    next_menu: str | None = None,
    btns_data: tuple[str, str] | None = None,
    level: int = 0,
    previous_menu: str = MAIN_MENU,
    region_id: int | None = None,
    size: tuple[int] = DEFAULT_KEYBOARD_SIZE,
    need_back_btn: bool = True,
    caption: str | None = None,
    callback_class: MenuCallBack | RegionAdminCallBack = MenuCallBack,
) -> tuple[InputMediaPhoto, InlineKeyboardMarkup]:
    """
    Aggregate function for creating a keyboard.
    Returns an image with a description and a keyboard for the menu.
    """
    return (
        await get_img(menu_name=menu_name, caption=caption),
        await get_btns(
            menu_name=menu_name,
            next_menu=next_menu,
            level=level,
            size=size,
            btns_data=btns_data,
            region_id=region_id,
            user_id=user_id,
            previous_menu=previous_menu,
            need_back_btn=need_back_btn,
            callback_class=callback_class,
        ),
    )
