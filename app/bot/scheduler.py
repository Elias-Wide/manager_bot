from datetime import datetime
import os

from aiogram.types import BufferedInputFile
from app.bot.handlers.callbacks.region_admin_menu import get_reports_info_by_region
from app.bot.init_bot import bot
from app.bot.keyboards.banners import get_file
from app.bot.utils import create_excel_report
from app.core.config import REPORTS_DIR
from app.core.constants import FMT_JPG
from app.points.dao import PointsDAO
from app.regions.dao import RegionsDAO
from app.reports.dao import ReportsDAO
from app.users.dao import UsersDAO
from app.users.models import Users


async def delete_reports_photo(dir: str = REPORTS_DIR, file_type: str = FMT_JPG):
    """
    Delete all files with the specified file_type (e.g., .jpeg) from the reports directory.

    Args:
        dir (str): Path to the reports directory.
        file_type (str): File extension to delete (e.g., '.jpeg').
    """
    for filename in os.listdir(dir):
        if filename.endswith(file_type):
            file_path = os.path.join(dir, filename)
            try:
                os.remove(file_path)
            except Exception as e:
                print(f"Error deleting file {file_path}: {e}")


async def notify_region_admins_about_missing_reports():
    """
    For each region:
    - Get all points with working schedule 'lower' and today's reports.
    - Find region admins.
    - For each point without a report, add to result list.
    - Send the list to each region admin.
    """
    regions = await RegionsDAO.get_multi()
    for region in regions:
        # points = await PointsDAO.get_objs_by_filter(region_id=region.id, working_schedule="middle")
        # reports = await ReportsDAO.get_reports_by_region(region.id, working_schedule="middle")
        # reports_dict = {r['point_id']: r for r in reports} if reports else {}

        admins: list[Users] = await UsersDAO.get_objs_by_filter(
            region_id=region.id, is_region_admin=True
        )
        if not admins:
            continue
        missing_reports = await get_reports_info_by_region(
            region_id=region.id, skeep_true=True, working_schedule="middle"
        )
        for admin in admins:
            if not missing_reports:
                await bot.send_photo(
                    chat_id=admin.telegram_id,
                    photo=await get_file("report_ok"),
                    caption="✅Все на рабочих местах👏",
                )
            else:
                excel_buffer = await create_excel_report(missing_reports)
                await bot.send_document(
                    chat_id=admin.telegram_id,
                    document=BufferedInputFile(
                        file=excel_buffer.getvalue(),
                        filename=f"Нет отчета прихода {datetime.now().date()}.xlsx",
                    ),
                )


async def get_reports_by_middle_schedule(region_id: int):
    pass
