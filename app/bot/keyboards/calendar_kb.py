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
    CHANGE_MONTH,
    CONFIRM_SCHEDULE_BTN,
    MONTH,
    NONE_MENU,
    PROFILE_MENU,
    SCHEDULE,
)

KeyboardMarkup: TypeAlias = InlineKeyboardMarkup | ReplyKeyboardMarkup


async def get_days_btns(
    *,
    user_id: int,
    level: int,
    user_schedule: list[date],
    size: int = CALENDAR_KEYBOARD_SIZE,
    month: int | None = None,
    previous_menu: str = PROFILE_MENU,
) -> list[InlineKeyboardButton]:
    """
    Создание клавиатуры календаря.
    Содержит даты текущего месяца, включая несколько дней
    пред. и след. месяцев для создания полных недель.
    """
    kb_builder = InlineKeyboardBuilder()
    btns = []
    today = datetime.now()
    print(f"{user_schedule=}")
    for month_number in range(month - 1, month + 2):
        text = f"{MONTH[month_number]}".lower()
        if month == month_number:
            text = text.upper()
        menu_name = CHANGE_MONTH
        if month_number < today.month or (month_number == month):
            menu_name = NONE_MENU
        btns.append(
            InlineKeyboardButton(
                text=text,
                callback_data=MenuCallBack(
                    level=level,
                    menu_name=menu_name,
                    user_id=user_id,
                    month=month_number,
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
                    menu_name=menu,
                    user_id=user_id,
                ).pack(),
            ),
        )
    for day in await get_month_days(today.year, month):
        text = day.strftime("%d")
        if day in user_schedule:
            text += "📍"
            user_schedule.remove(day)
        btns.append(
            InlineKeyboardButton(
                text=text,
                callback_data=MenuCallBack(
                    level=level,
                    menu_name=SCHEDULE,
                    user_id=user_id,
                    month=month,
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


async def get_month_days(year: int, month: int) -> list[date]:
    """
    Возвращает список дней текущего месяца.
    Дополнительно содержит несколько дней прошлого и след. месяцев
    для генерации полной недели."""
    return [day for day in Calendar().itermonthdates(year, month)]
