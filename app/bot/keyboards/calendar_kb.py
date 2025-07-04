from calendar import Calendar
from datetime import date, datetime
from typing import TypeAlias

from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.core.constants import CALENDAR_KEYBOARD_SIZE
from app.bot.handlers.callbacks.menucallback import MenuCallBack
from app.bot.keyboards.buttons import (
    BACK_BTN,
    CALENDAR_BTNS,
    CONFIRM_SCHEDULE_BTN,
    MONTH,
    PROFILE_MENU,
    SCHEDULE,
)

KeyboardMarkup: TypeAlias = InlineKeyboardMarkup | ReplyKeyboardMarkup


async def get_days_btns(
    *,
    user_id: int,
    level: int,
    user_schedule: list[date],
    menu_name: str = SCHEDULE,
    size: int = CALENDAR_KEYBOARD_SIZE,
    previous_menu: str = PROFILE_MENU,
) -> list[InlineKeyboardButton]:
    """
    Создание клавиатуры календаря.
    Содержит даты текущего месяца, включая несколько дней
    пред. и след. месяцев для создания полных недель.
    """
    kb_builder = InlineKeyboardBuilder()
    btns = []
    now = datetime.now()
    for month_number in range(now.month - 1, now.month + 2):
        text = f"{MONTH[month_number]}".lower()
        if month_number == now.month:
            text = text.upper()
        btns.append(
            InlineKeyboardButton(
                text=text,
                callback_data=MenuCallBack(
                    level=level,
                    menu_name=menu_name,
                    user_id=user_id,
                ).pack(),
            ),
        )
    kb_builder.row(*btns, width=3)
    btns = []
    for menu, text in CALENDAR_BTNS:
        btns.append(
            InlineKeyboardButton(
                text=text,
                callback_data=MenuCallBack(
                    level=level,
                    menu_name=menu_name,
                    user_id=user_id,
                ).pack(),
            ),
        )
    for day in await get_current_month_days():
        text = day.strftime("%d")
        if day in user_schedule:
            text += "📍"
            user_schedule.remove(day)
        btns.append(
            InlineKeyboardButton(
                text=text,
                callback_data=MenuCallBack(
                    level=level,
                    menu_name=menu_name,
                    user_id=user_id,
                    day=day.strftime("%m.%d.%Y"),
                ).pack(),
            ),
        )
    btns.append(
        InlineKeyboardButton(
            text=BACK_BTN,
            callback_data=MenuCallBack(
                user_id=user_id,
                level=level,
                menu_name=PROFILE_MENU,
            ).pack(),
        )
    )
    btns.append(
        InlineKeyboardButton(
            text=CONFIRM_SCHEDULE_BTN[1],
            callback_data=MenuCallBack(
                user_id=user_id,
                level=level,
                menu_name=CONFIRM_SCHEDULE_BTN[0],
            ).pack(),
        )
    )
    kb_builder.row(*btns, width=size)
    return kb_builder.as_markup()


async def get_current_month_days() -> list[date]:
    """
    Возвращает список дней текущего месяца.
    Дополнительно содержит несколько дней прошлого и след. месяцев
    для генерации полной недели."""
    now = datetime.now()
    days = Calendar()
    return [day for day in Calendar().itermonthdates(now.year, now.month)]
