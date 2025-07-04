from datetime import datetime
from sqlalchemy import and_, func, select
from app.dao.base import BaseDAO
from app.core.database import async_session_maker
from app.points.models import Points
from app.reports.models import Reports
from app.users.models import Users


class ReportsDAO(BaseDAO):
    """
    A class for CRUD operations with Reports.

    This class provides methods for interacting with the `Reports` model.
    """

    model = Reports

    @classmethod
    async def get_reports_by_region(
        cls, region_id: int, working_schedule: str | None = None
    ) -> list[Reports] | None:
        stmt = and_(
            Reports.created_at_date == datetime.now().date(),
            Points.region_id == region_id,
        )
        if working_schedule:
            stmt = and_(
                Reports.created_at_date == datetime.now().date(),
                Points.region_id == region_id,
                Points.working_schedule == working_schedule,
            )
        async with async_session_maker() as session:
            reports = await session.execute(
                select(*reports_attrs_to_get)
                .join(Reports, Points.id == Reports.point_id, isouter=True)
                .join(Users, Users.id == Reports.user_id)
                .where(stmt)
                .order_by("created_at")
            )
            return reports.mappings().all() if reports else []

    @classmethod
    async def get_today_point_report(
        cls,
        point_id: int,
    ) -> Reports | None:
        async with async_session_maker() as session:
            stmt = (
                select(*reports_attrs_to_get)
                .join(Points, Points.id == Reports.point_id)
                .join(Users, Users.id == Reports.user_id)
                .where(
                    and_(
                        Reports.point_id == point_id,
                        Reports.created_at_date == datetime.now().date(),
                    )
                )
            )
            report = await session.execute(stmt)
            return report.mappings().first() if report else None


reports_attrs_to_get = (
    Reports.__table__.columns,
    Points.id,
    Points.addres,
    Users.first_name,
    Users.last_name,
    Users.username,
)
