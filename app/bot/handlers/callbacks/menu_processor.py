from aiogram.types import InlineKeyboardMarkup, InputMediaPhoto

from app.bot.keyboards.buttons import (
    MAIN_MENU,
    MAIN_MENU_BUTTONS,
    PROFILE_MENU,
    PROFILE_MENU_BTNS,
)
from app.bot.keyboards.captions import get_user_full_data
from app.bot.keyboards.main_kb_builder import get_image_and_kb


# async def get_main_menu(
#     level: int, menu_name: str, user_id: int, point_id: int | None = None
# ) -> tuple[InputMediaPhoto, InlineKeyboardMarkup]:
#     return await get_image_and_kb(
#         menu_name=menu_name,
#         user_id=user_id,
#         point_id=point_id,
#         btns_data=MAIN_MENU_BUTTONS,
#         level=level,
#         need_back_btn=False,
#     )


async def get_menu_content(
    menu_name: str,
    level: int,
    user_id: int,
) -> tuple[InputMediaPhoto | InlineKeyboardMarkup]:
    if menu_name == MAIN_MENU:
        return await get_image_and_kb(
            menu_name=menu_name,
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
