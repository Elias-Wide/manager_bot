from sqlalchemy import and_, func, insert, select
from app.dao.base import BaseDAO
from app.core.database import async_session_maker
from app.points.models import Points


class PointsDAO(BaseDAO):
    model = Points

    @classmethod
    async def search_by_addres(cls, searching_address: str):
        async with async_session_maker() as session:
            get_objs = await session.execute(
                select(cls.model.__table__.columns)
                .where(
                    and_(
                        func.lower(Points.addres).contains(
                            searching_address.lower(),
                        ),
                        Points.id != 1,
                    )
                )
                .order_by("addres")
            )
            return get_objs.mappings().all()

    @classmethod
    async def get_points_by_region_id(cls, region_id: int):
        async with async_session_maker() as session:
            get_objs = await session.execute(
                select(cls.model.__table__.columns)
                .where(Points.region_id == region_id)
                .order_by("point_id")
            )
            return get_objs.mappings().all()
