from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery, Message

from app.bot.filters import RegionPointFilter
from app.bot.handlers.callbacks.menucallback import RegionAdminCallBack
from app.bot.handlers.callbacks.region_admin_menu import (
    get_all_reports,
    get_day_reports_by_region,
)
from app.bot.keyboards.banners import get_file
from app.bot.keyboards.buttons import (
    ALL_PHOTOS,
    CRITICAL_ERROR,
    GET_DAY_REPORT,
    GET_OFFICE_MANAGERS,
    GET_OFFICE_REPORT,
    WB_ADMIN_MENU_BTNS,
    WB_ADMIN_MENU_PAGES,
)
from app.bot.keyboards.captions import captions
from app.bot.keyboards.main_kb_builder import get_btns
from app.bot.states import ReportsStates
from app.core.config import REPORTS_DIR
from app.points.models import Points
from app.regions.dao import RegionsDAO
from app.reports.dao import ReportsDAO
from app.reports.models import Reports
from app.bot.scheduler import (
    delete_reports_photo,
    notify_region_admins_about_missing_reports,
)
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
    RegionAdminCallBack.filter(F.menu_name.in_(WB_ADMIN_MENU_PAGES)),
    default_state,
)
async def get_region_admin_menu(
    callback: CallbackQuery,
    callback_data: RegionAdminCallBack,
    state: FSMContext,
):
    user: Users = await UsersDAO.get_by_attribute("telegram_id", callback.from_user.id)
    try:
        if callback_data.menu_name == ALL_PHOTOS:
            await get_all_reports(callback, callback_data)
        elif callback_data.menu_name == GET_OFFICE_REPORT:
            await state.set_state(ReportsStates.choose_report_office)
            await callback.message.answer(text=captions.choose_office)
        elif callback_data.menu_name == GET_DAY_REPORT:
            await get_day_reports_by_region(callback, callback_data)
        elif callback_data.menu_name == GET_OFFICE_MANAGERS:
            await callback.message.answer(captions.choose_office)
            await state.set_state(ReportsStates.office_info)
        await callback.answer()
    except Exception as error:
        print(error)
        await callback.answer(text=CRITICAL_ERROR, show_alert=True)


@region_admin_router.message(
    ReportsStates.choose_report_office,
    F.text.regexp(r"^\d+$"),
    RegionPointFilter(),
)
async def choose_report_point(message: Message, state: FSMContext, point: Points):
    report: Reports = await ReportsDAO.get_today_point_report(point.id)
    await state.set_state(default_state)
    if not report:
        await message.answer("Отчет не найден.")
        return
    await message.answer_photo(
        photo=await get_file(
            filename=report.img,
            file_dir=REPORTS_DIR,
        ),
        caption=await captions.get_office_report_caption(report),
    )


@region_admin_router.message(
    ReportsStates.office_info,
    F.text.regexp(r"^\d+$"),
    RegionPointFilter(),
)
async def choose_office_info(message: Message, state: FSMContext, point: Points):
    managers: Users = await UsersDAO.get_objs_by_filter(point_id=point.id)
    await message.answer(text=await captions.get_office_info(point, managers))
    await state.set_state(default_state)


@region_admin_router.message(
    ReportsStates.choose_report_office, ~F.text.regexp(r"^\d+$")
)
@region_admin_router.message(ReportsStates.office_info, ~F.text.regexp(r"^\d+$"))
async def incorrect_report_point_id_format_handler(message: Message, state: FSMContext):
    await message.answer(captions.incorrect_point_id_format)


@region_admin_router.message(
    ReportsStates.choose_report_office,
    F.text.regexp(r"^\d+$"),
    ~RegionPointFilter(),
)
@region_admin_router.message(
    ReportsStates.office_info,
    F.text.regexp(r"^\d+$"),
    ~RegionPointFilter(),
)
async def handle_office_not_in_region(message: Message, state: FSMContext):
    await message.answer(captions.office_not_in_region)


@region_admin_router.message(Command("delete"))
async def deletefdf(message: Message, state: FSMContext):
    await delete_reports_photo()


@region_admin_router.message(Command("send"))
async def notify(message: Message, state: FSMContext):
    await notify_region_admins_about_missing_reports(
        working_schedule=None, skeep_true=False
    )
