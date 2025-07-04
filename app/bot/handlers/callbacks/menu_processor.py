from aiogram.types import InlineKeyboardMarkup, InputMediaPhoto

from app.bot.keyboards.buttons import (
    MAIN_MENU,
    MAIN_MENU_BUTTONS,
    PROFILE_MENU,
    PROFILE_MENU_BTNS,
    REPORTS_MENU,
    REPORTS_MENU_BTNS,
)
from app.bot.keyboards.captions import get_user_full_data
from app.bot.keyboards.main_kb_builder import get_image_and_kb


async def get_menu_content(
    menu_name: str,
    level: int,
    user_id: int,
) -> tuple[InputMediaPhoto | InlineKeyboardMarkup]:
    print(f"get_menu_content: {menu_name=}, {level=}, {user_id=}")
    if menu_name == MAIN_MENU:
        return await get_image_and_kb(
            menu_name=menu_name,
            level=0,
            user_id=user_id,
            need_back_btn=False,
            btns_data=MAIN_MENU_BUTTONS,
        )
    elif menu_name == PROFILE_MENU:
        return await get_image_and_kb(
            menu_name=PROFILE_MENU,
            user_id=user_id,
            need_back_btn=True,
            btns_data=PROFILE_MENU_BTNS,
            caption=await get_user_full_data(user_id=user_id),
        )
    elif menu_name == REPORTS_MENU:
        return await get_image_and_kb(
            menu_name=menu_name,
            user_id=user_id,
            need_back_btn=True,
            btns_data=REPORTS_MENU_BTNS,
        )
