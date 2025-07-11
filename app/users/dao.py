from datetime import datetime
from typing import List

from asyncache import cached
from cachetools import TTLCache
from sqlalchemy import and_, extract, func, select

from app.core.database import async_session_maker
from app.dao.base import BaseDAO
from app.offices.models import Offices
from app.users.models import Users, WorkDays

user_cache = TTLCache(maxsize=128, ttl=30)
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
                    Offices.id.label("office_id"),
                    Offices.addres,
                )
                .join(Offices, Offices.id == Users.office_id, isouter=True)
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
    async def get_workday_manager(cls, office_id: int) -> list[Users] | None:
        async with async_session_maker() as session:
            today = datetime.now().date()
            stmt = (
                select(
                    Users,
                    Offices.__table__.columns,
                    WorkDays.day,
                )
                .join(WorkDays, WorkDays.user_id == Users.id)
                .join(Offices, Offices.id == Users.office_id)
                .where(
                    and_(
                        Users.office_id == office_id,
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
    async def get_user_working_days(cls, user_id: int, month: int) -> list[WorkDays]:
        async with async_session_maker() as session:
            work_days = await session.execute(
                select(cls.model)
                .where(
                    and_(
                        cls.model.user_id == user_id,
                        extract("month", WorkDays.day) == month,
                    )
                )
                .order_by("day")
            )
            return work_days.scalars().all()

    @classmethod
    async def set_user_schedule(
        cls, user_id: int, work_days: List[datetime.date]
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

    @classmethod
    async def get_region_schedule(cls, region_id: int) -> List[dict]:

        async with async_session_maker() as session:
            stmt = (
                select(WorkDays.day, Offices.addres, Offices.id.label("office_id"))
                .join(Offices, Offices.region_id == region_id)
                .join(Users, Users.office_id == Offices.id)
                .where(
                    and_(
                        extract("month", WorkDays.day) == datetime.now().month,
                    )
                )
            )
            workdays_list = await session.execute(stmt)
            return workdays_list.mappings().all()
