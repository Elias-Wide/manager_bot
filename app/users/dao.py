import datetime
from sqlalchemy import select

from app.core.database import async_session_maker
from app.dao.base import BaseDAO
from app.points.models import Points
from app.users.models import Users, WorkDays


class UsersDAO(BaseDAO):
    """
    A class for CRUD operations with users.

    This class provides methods for interacting with the `Users` model.
    """

    model = Users

    @classmethod
    async def get_user_full_data(cls, user_id: int):
        """
        Запрос в базу данных для получения полной информации.
        Возвращает данные о пользователе по телеграм id,
        включаюя данные рабочего офиса пользователя.
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
