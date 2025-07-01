import datetime
from sqlalchemy import select
from app.dao.base import BaseDAO
from app.core.database import async_session_maker
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
            get_user = await session.execute(
                select(
                    Users.__table__.columns,
                    Points.id.label("point_id"),
                    Points.addres,
                )
                .join(Points, Points.id == Users.point_id, isouter=True)
                .where(Users.id == user_id)
            )
        data = get_user.mappings().all()[0]
        print(data)
        return data


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
    async def set_user_schedule(cls, user_id, work_days: list[datetime.date]) -> None:
        async with async_session_maker() as session:
            work_days = [cls.model(user_id=user_id, day=day) for day in work_days]
            session.add_all(work_days)
            await session.commit()
