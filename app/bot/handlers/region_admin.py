from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery, Message

from app.bot.filters import RegionPointFilter
from app.bot.handlers.callbacks.menucallback import RegionAdminCallBack
from app.bot.handlers.callbacks.region_admin_menu import get_all_reports
from app.bot.keyboards.banners import get_file
from app.bot.keyboards.buttons import (
    ALL_PHOTOS,
    GET_DAY_REPORT,
    GET_OFFICE_REPORT,
    WB_ADMIN_MENU_BTNS,
    WB_ADMIN_MENU_PAGES,
)
from app.bot.keyboards.captions import captions
from app.bot.keyboards.main_kb_builder import get_btns
from app.bot.states import ReportsStates
from app.points.models import Points
from app.regions.dao import RegionsDAO
from app.reports.dao import ReportsDAO
from app.reports.models import Reports
from app.users.dao import UsersDAO
from app.users.models import Users

region_admin_router = Router()
region_admin_router.message.filter()


@region_admin_router.message(Command("wb_admin"))
async def region_admin_menu(
    message: Message,
) -> None:
    """
    Start command handler for the WB admin bot.
    Initializes the bot and sets the state to the main menu.
    """
    user: Users = await UsersDAO.get_by_attribute(
        attr_name="telegram_id", attr_value=message.from_user.id
    )
    region = await RegionsDAO.get_by_attribute(attr_name="ceo_id", attr_value=user.id)
    await message.answer_photo(
        photo=await get_file("wb_admin_menu"),
        caption=captions.no_caption,
        reply_markup=await get_btns(
            menu_name="wb_admin_menu",
            user_id=user.id,
            btns_data=WB_ADMIN_MENU_BTNS,
            level=0,
            need_back_btn=False,
            region_id=region.id,
            callback_class=RegionAdminCallBack,
        ),
    )


@region_admin_router.callback_query(
    RegionAdminCallBack.filter(F.menu_name.in_(WB_ADMIN_MENU_PAGES)), default_state
)
async def get_region_admin_menu(
    callback: CallbackQuery, callback_data: RegionAdminCallBack, state: FSMContext
):
    if callback_data.menu_name == ALL_PHOTOS:
        await get_all_reports(callback, callback_data)
    elif callback_data.menu_name == GET_OFFICE_REPORT:
        await state.set_state(ReportsStates.choose_report_office)
        await callback.message.answer(text=captions.choose_office)
    elif callback_data.menu_name == GET_DAY_REPORT:
        pass


@region_admin_router.message(
    ReportsStates.choose_report_office, F.text.regexp(r"^\d+$"), RegionPointFilter()
)
async def choose_report_office(message: Message, state: FSMContext, point: Points):
    # report: Reports = await ReportsDAO.get_by_attribute("point_id")
    await message.answer("Лови")


@region_admin_router.message(
    ReportsStates.choose_report_office, ~F.text.regexp(r"^\d+$")
)
async def incorrect_report_office_id_format_handler(
    message: Message, state: FSMContext
):
    await message.answer(captions.incorrect_point_id_format)


@region_admin_router.message(
    ReportsStates.choose_report_office, F.text.regexp(r"^\d+$"), ~RegionPointFilter()
)
async def incorrect_report_office_id_handler(message: Message, state: FSMContext):
    await message.answer(captions.point_not_in_region)
