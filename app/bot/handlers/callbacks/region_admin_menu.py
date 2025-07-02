from aiogram.types import CallbackQuery, Message

from app.bot.handlers.callbacks.menucallback import RegionAdminCallBack
from app.bot.keyboards.banners import get_file
from app.bot.keyboards.captions import captions
from app.core.config import REPORTS_DIR
from app.core.constants import FMT_JPG
from app.reports.dao import ReportsDAO
from app.users.dao import UsersDAO


async def get_all_reports(
    callback: CallbackQuery,
    callback_data: RegionAdminCallBack,
):
    print(f"{callback_data.region_id=}")
    reports = await ReportsDAO.get_reports_by_region(region_id=callback_data.region_id)
    print(reports)
    if reports:
        for report in reports:
            await callback.message.answer_photo(
                photo=await get_file(
                    filename=report.img,
                    file_dir=REPORTS_DIR,
                ),
                caption=await captions.get_office_report_caption(report),
            )
