from calendar import Calendar
from datetime import date, datetime
from typing import TypeAlias

from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           ReplyKeyboardMarkup)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.bot.handlers.subfunctions.menucallback import MenuCallBack
from app.bot.keyboards.buttons import (BACK_BTN, CALENDAR_BTNS, CHANGE_MONTH,
                                       CONFIRM_SCHEDULE_BTN, MONTH, NONE_MENU,
                                       PROFILE_MENU, SCHEDULE)
from app.core.constants import CALENDAR_KEYBOARD_SIZE

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
    Create a calendar keyboard.

    This function generates a calendar keyboard for the current month,
    including several days from the previous and next months to form complete weeks.
    The keyboard highlights days from the user's schedule and provides navigation buttons.

    Args:
        user_id (int): The user's Telegram ID.
        level (int): The menu level for callback data.
        user_schedule (list[date]): List of dates to highlight in the calendar.
        size (int, optional): Number of buttons per row. Defaults to CALENDAR_KEYBOARD_SIZE.
        month (int | None, optional): The month to display. Defaults to current month.
        previous_menu (str, optional): The name of the previous menu for navigation. Defaults to PROFILE_MENU.

    Returns:
        list[InlineKeyboardButton]: List of inline keyboard buttons representing the calendar.
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
    Return a list of days for the given month.

    This function returns all days of the specified month,
    including extra days from the previous and next months to generate full weeks.

    Args:
        year (int): The year.
        month (int): The month.

    Returns:
        list[date]: List of date objects for the calendar view.
    """
    return [day for day in Calendar().itermonthdates(year, month)]
