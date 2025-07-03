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
    async def get_reports_by_region(cls, region_id: int) -> list[Reports] | None:
        async with async_session_maker() as session:
            reports = await session.execute(
                select(
                    Reports.__table__.columns,
                    Points.__table__.columns,
                    Users.first_name,
                    Users.last_name,
                    Users.username,
                )
                .join(Reports, Points.id == Reports.point_id, isouter=True)
                .join(Users, Users.id == Reports.user_id)
                .where(
                    and_(
                        func.date(Reports.created_at) == datetime.now().date(),
                        Points.region_id == region_id,
                    )
                )
            )
            return reports.mappings().all() if reports else None

    @classmethod
    async def get_today_point_report(
        cls,
        point_id: int,
    ) -> Reports | None:
        async with async_session_maker() as session:
            stmt = select(Reports.__table__.columns).where(Reports.point_id == point_id)
