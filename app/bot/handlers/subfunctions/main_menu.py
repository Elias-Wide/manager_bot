from aiogram.types import CallbackQuery, Message

from app.bot.handlers.subfunctions.menu_processor import get_menu_content
from app.bot.handlers.subfunctions.menucallback import MenuCallBack
from app.bot.keyboards.buttons import CRITICAL_ERROR, MAIN_MENU
from app.users.dao import UsersDAO


async def procces_main_menu_comand(
    message: Message, level: int = 0, menu_name: str = MAIN_MENU
) -> None:
    try:
        user = await UsersDAO.get_by_tg_id(message.from_user.id)

        media, reply_markup = await get_menu_content(
            level=level, menu_name=menu_name, user=user
        )
        await message.answer_photo(
            photo=media.media,
            caption=media.caption,
            reply_markup=reply_markup,
        )
    except Exception as error:
        print(error)
        await message.answer(text=CRITICAL_ERROR)


async def get_menu(
    callback: CallbackQuery, callback_data: MenuCallBack
) -> None:
    user = await UsersDAO.get_by_tg_id(callback.from_user.id)
    callback_data.user_id = user.id
    media, reply_markup = await get_menu_content(
        level=callback_data.level, menu_name=callback_data.menu_name, user=user
    )
    await callback.message.edit_media(
        media=media,
        reply_markup=reply_markup,
    )
