from datetime import datetime
from aiogram.types import BufferedInputFile, CallbackQuery

from app.bot.handlers.callbacks.menucallback import RegionAdminCallBack
from app.bot.keyboards.banners import get_file
from app.bot.keyboards.captions import captions
from app.bot.utils import create_excel_report
from app.core.config import REPORTS_DIR
from app.points.dao import PointsDAO
from app.points.models import Points
from app.reports.dao import ReportsDAO
from app.reports.models import Reports
from app.users.dao import UsersDAO


async def get_all_reports(
    callback: CallbackQuery,
    callback_data: RegionAdminCallBack,
) -> None:
    reports = await ReportsDAO.get_reports_by_region(region_id=callback_data.region_id)
    if reports:
        for report in reports:
            await callback.message.answer_photo(
                photo=await get_file(
                    filename=report.img,
                    file_dir=REPORTS_DIR,
                ),
                caption=await captions.get_office_report_caption(report),
            )
    else:
        await callback.message.answer(text=captions.no_reports_today)


async def get_day_reports_by_region(
    callback: CallbackQuery,
    callback_data: RegionAdminCallBack,
) -> None:
    excel_buffer = await create_excel_report(
        await get_reports_info_by_region(region_id=callback_data.region_id)
    )
    await callback.message.answer_document(
        document=BufferedInputFile(
            file=excel_buffer.getvalue(),
            filename=f"Отчеты прихода {datetime.now().date()}.xlsx",
        )
    )


async def get_reports_info_by_region(
    region_id: int,
    skeep_true: bool = False,
    working_schedule: str | None = None,
) -> list[tuple[str]] | None:
    region_reports_data = []
    reports: dict[int:Reports] = {
        report.point_id: report
        for report in (
            await ReportsDAO.get_reports_by_region(
                region_id=region_id, working_schedule=working_schedule
            )
        )
    }
    print(f"{reports=}")
    offices_by_region: tuple[Points] = tuple(
        sorted(
            await PointsDAO.get_points_by_region_id(
                region_id=region_id, working_schedule=working_schedule
            ),
            key=lambda x: x.working_schedule == "middle",
        )
    )
    for office in offices_by_region:
        office: Points = office
        if office.id in reports and not skeep_true:
            report = reports[office.id]
            created_at = report["created_at"]
            region_reports_data.append(
                (
                    report["addres"],
                    report["point_id"],
                    f'{report["first_name"]} {report["last_name"]} (@{report["username"]})',
                    created_at,
                    office.working_schedule.value,
                )
            )
        elif office.id not in reports:
            managers = await UsersDAO.get_workday_manager(office.id)
            if not managers:
                managers = "-"
            region_reports_data.append(
                (
                    office.addres,
                    office.id,
                    managers,
                    False,
                    office.working_schedule.value,
                )
            )
    return list(sorted(region_reports_data, key=lambda r: bool(r[3])))
