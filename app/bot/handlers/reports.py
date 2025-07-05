from datetime import datetime
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery, Message

from app.bot.filters import PointExistFilter, ValidatePhotoFilter
from app.bot.handlers.callbacks.menucallback import MenuCallBack
from app.bot.keyboards.captions import captions
from app.bot.keyboards.banners import get_img
from app.bot.keyboards.buttons import (
    CHOOSE_OFFICE,
    CRITICAL_ERROR,
    MY_OFFICE_REPORT,
    OTHER_OFFICE_REPORT,
    REPORTS_MENU,
)
from app.bot.keyboards.main_kb_builder import get_btns
from app.bot.states import ReportsStates
from app.points.models import Points
from app.reports.dao import ReportsDAO
from app.users.dao import UsersDAO
from app.users.models import Users

reports_router = Router()


@reports_router.callback_query(
    MenuCallBack.filter(
        F.menu_name.in_(
            OTHER_OFFICE_REPORT,
        )
    ),
    default_state,
)
async def choose_office(
    callback: CallbackQuery,
    callback_data: MenuCallBack,
    state: FSMContext,
) -> None:
    """
    Handles the button click for selecting an office for the report.
    Proceeds to the next state for office selection.
    """
    print(f"{callback_data=}")
    await state.set_state(ReportsStates.choose_office)
    await callback.message.edit_media(
        media=await get_img(CHOOSE_OFFICE),
        reply_markup=await get_btns(
            menu_name=REPORTS_MENU,
            previous_menu=REPORTS_MENU,
            level=2,
            need_back_btn=True,
        ),
    )


@reports_router.message(
    Command("get_work"),
)
async def get_work_handler(
    message: Message,
    state: FSMContext,
) -> None:
    """
    Handles the /get_work command.
    Prompts the user to select an office for the report.
    """
    await office_report_mixin(callback=message, state=state)


@reports_router.callback_query(
    MenuCallBack.filter(
        F.menu_name.in_(
            MY_OFFICE_REPORT,
        )
    ),
    default_state,
)
async def my_office_report_handler(
    callback: CallbackQuery,
    callback_data: MenuCallBack,
    state: FSMContext,
) -> None:
    await office_report_mixin(callback, state, callback_data)


async def office_report_mixin(
    callback: Message | CallbackQuery,
    state: FSMContext,
    callback_data: MenuCallBack | None = None,
) -> None:
    user: Users = await UsersDAO.get_by_attribute(
        attr_name="telegram_id",
        attr_value=callback.from_user.id,
    )
    user_data = await UsersDAO.get_user_full_data(user_id=user.id)
    await state.update_data(
        point_id=user_data["point_id"],
        addres=user_data["addres"],
        user_id=user.id,
    )
    await state.set_state(ReportsStates.send_photo)
    if callback_data:
        callback = callback.message
    await callback.answer(
        text=captions.send_photo.format(
            addres=user_data["addres"], point_id=user_data["point_id"]
        )
    )


@reports_router.message(
    ReportsStates.choose_office, F.text.isdigit(), PointExistFilter()
)
async def send_report_photo(message: Message, state: FSMContext, point: Points) -> None:
    """
    Handles input of office ID for the report.
    Proceeds to the next state for sending the report photo.
    """
    point_id = int(message.text)
    await state.update_data(point_id=point_id, addres=point.addres)
    await state.set_state(ReportsStates.send_photo)
    await message.answer(
        text=captions.send_photo.format(addres=point.addres, point_id=point.id)
    )


@reports_router.message(
    ReportsStates.choose_office, F.text.isdigit(), ~PointExistFilter()
)
async def incorrect_office_id_handler(message: Message, state: FSMContext) -> None:
    """
    Handles incorrect office ID input.
    Sends an error message.
    """
    await message.answer(text="Офис отсутствует в базе данных.")


@reports_router.message(ReportsStates.choose_office, ~F.text.isdigit())
async def incorrect_office_id_format_handler(
    message: Message, state: FSMContext
) -> None:
    """
    Handles incorrect office ID format.
    Sends an error message.
    """
    await message.answer(text="Допускаются только цифры.")


@reports_router.message(ReportsStates.send_photo, F.photo, ValidatePhotoFilter())
async def send_report_photo_handler(
    message: Message, state: FSMContext, img_name: str
) -> None:
    """
    Handles sending a report photo.
    Saves the photo and proceeds to the next state.
    """
    state_data = await state.get_data()
    point_id = state_data.get("point_id")
    photo = message.photo[-1]

    try:
        await ReportsDAO.create(
            {
                "user_id": state_data.get(
                    "user_id",
                    (
                        await UsersDAO.get_by_attribute(
                            attr_name="telegram_id",
                            attr_value=message.from_user.id,
                        )
                    ).id,
                ),
                "created_at": datetime.now(),
                "point_id": state_data["point_id"],
                "img": img_name,
            }
        )
        await message.answer(text=captions.reports_success)
        await state.clear()
    except Exception as error:
        print(error)
        if "unique_report_in_a_day" in str(error):
            await message.answer(
                text=captions.report_created_today.format(addres=state_data["addres"])
            )
        else:
            await message.answer(text=CRITICAL_ERROR, show_alert=True)


@reports_router.message(ReportsStates.send_photo, ~F.photo)
async def incorrect_photo_handler(
    message: Message,
    state: FSMContext,
) -> None:
    """
    Handles incorrect report photo format.
    Sends an error message.
    """
    state_data = await state.get_data()
    await message.answer(
        text=captions.reports_incorrect_photo_format.format(addres=state_data["addres"])
    )
