from datetime import datetime
from sqlalchemy import and_, select
from asyncache import cached
from cachetools import TTLCache

from app.core.database import async_session_maker
from app.dao.base import BaseDAO
from app.points.models import Points
from app.users.models import Users, WorkDays

# Cache for get_user_full_data: 128 keys, 600 seconds TTL
user_cache = TTLCache(maxsize=128, ttl=150)
workday_manager_cache = TTLCache(maxsize=128, ttl=300)


class UsersDAO(BaseDAO):
    """
    A class for CRUD operations with users.

    This class provides methods for interacting with the `Users` model.
    """

    model = Users

    @classmethod
    @cached(user_cache)
    async def get_user_full_data(cls, user_id: int):
        """
        Query the database to get full user information.
        Returns user data by telegram id, including office data.
        """
        async with async_session_maker() as session:
            user = await session.execute(
                select(
                    Users.__table__.columns,
                    Points.id.label("point_id"),
                    Points.addres,
                )
                .join(Points, Points.id == Users.point_id, isouter=True)
                .where(Users.id == user_id)
            )
        if user:
            return user.mappings().all()[0]

    @classmethod
    @cached(user_cache)
    async def get_by_tg_id(cls, telegram_id: int) -> Users | None:
        """
        Get a user by their Telegram ID.
        """
        return await BaseDAO.get_by_attribute(
            attr_name="telegram_id", attr_value=telegram_id
        )

    @classmethod
    @cached(workday_manager_cache)
    async def get_workday_manager(cls, point_id: int) -> list[Users] | None:
        async with async_session_maker() as session:
            today = datetime.now().date()
            stmt = (
                select(
                    Users,
                    Points.__table__.columns,
                    WorkDays.day,
                )
                .join(WorkDays, WorkDays.user_id == Users.id)
                .join(Points, Points.id == Users.point_id)
                .where(
                    and_(
                        Users.point_id == point_id,
                        WorkDays.day == datetime.now().date(),
                    )
                )
            )
            managers = await session.execute(stmt)
            managers = managers.scalars().all()
            return managers if managers else []


class WorkDaysDAO(BaseDAO):

    model = WorkDays

    @classmethod
    async def get_user_working_days(cls, user_id: int) -> list[WorkDays]:
        async with async_session_maker() as session:
            work_days = await session.execute(
                select(cls.model).where(cls.model.user_id == user_id)
            )
            return work_days.scalars().all()

    @classmethod
    async def set_user_schedule(
        cls, user_id: int, work_days: list[datetime.date]
    ) -> None:
        """
        Replace all workdays for a user with a new list using bulk create.
        """
        async with async_session_maker() as session:
            await session.execute(
                WorkDays.__table__.delete().where(WorkDays.user_id == user_id)
            )
            if work_days:
                work_days_objs = [
                    WorkDays(user_id=user_id, day=day) for day in work_days
                ]
                session.add_all(work_days_objs)
            await session.commit()
