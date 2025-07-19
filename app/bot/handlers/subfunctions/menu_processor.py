from aiogram.types import InlineKeyboardMarkup, InputMediaPhoto

from app.bot.keyboards.buttons import (
    MAIN_MENU,
    MAIN_MENU_BUTTONS,
    PROFILE_MENU,
    PROFILE_MENU_BTNS,
    REPORTS_MENU,
    REPORTS_MENU_BTNS,
    REPORTS_MENU_BTNS_MINI,
)
from app.bot.keyboards.captions import get_user_full_data
from app.bot.keyboards.main_kb_builder import get_image_and_kb
from app.offices.constants import NO_OFFICE_ID
from app.users.models import Users


async def get_menu_content(
    menu_name: str,
    level: int,
    user: Users,
) -> tuple[InputMediaPhoto | InlineKeyboardMarkup]:
    if menu_name == MAIN_MENU:
        return await get_image_and_kb(
            menu_name=menu_name,
            level=0,
            user_id=user.id,
            need_back_btn=False,
            btns_data=MAIN_MENU_BUTTONS,
        )
    elif menu_name == PROFILE_MENU:
        return await get_image_and_kb(
            menu_name=PROFILE_MENU,
            user_id=user.id,
            need_back_btn=True,
            btns_data=PROFILE_MENU_BTNS,
            caption=await get_user_full_data(user_id=user.id),
        )
    elif menu_name == REPORTS_MENU:
        btns_data = REPORTS_MENU_BTNS
        if user.office_id == NO_OFFICE_ID:
            btns_data = REPORTS_MENU_BTNS_MINI
        return await get_image_and_kb(
            menu_name=menu_name,
            user_id=user.id,
            need_back_btn=True,
            btns_data=btns_data,
        )
