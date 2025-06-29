"""Клавиатура вступительной анкеты."""

from typing import Iterable, TypeAlias

from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.bot.keyboards.buttons import CONFIRM_REGISTRATION
from app.core.constants import DEFAULT_KEYBOARD_SIZE, MAIN_MENU

KeyboardMarkup: TypeAlias = InlineKeyboardMarkup | ReplyKeyboardMarkup


async def create_registration_kb(
    size: int = DEFAULT_KEYBOARD_SIZE,
) -> KeyboardMarkup:
    """Create a keyboard for the start of registration process."""
    kb_builder = InlineKeyboardBuilder()
    btns = []
    for text, callback_datas in zip(
        dict(CONFIRM_REGISTRATION).values(), dict(CONFIRM_REGISTRATION).keys()
    ):
        btns.append(
            InlineKeyboardButton(text=text, callback_data=callback_datas),
        )
    kb_builder.row(*btns, width=size)
    return kb_builder.as_markup()
