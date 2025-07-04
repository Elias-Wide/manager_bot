from sqlalchemy import and_, func, insert, select
from app.dao.base import BaseDAO
from app.core.database import async_session_maker
from app.points.models import Points


class PointsDAO(BaseDAO):
    model = Points

    @classmethod
    async def search_by_addres(cls, searching_address: str):
        async with async_session_maker() as session:
            stmt = await session.execute(
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
            return stmt.mappings().all()

    @classmethod
    async def get_points_by_region_id(cls, region_id: int):
        async with async_session_maker() as session:
            stmt = await session.execute(
                select(cls.model.__table__.columns).where(Points.region_id == region_id)
            )
            return stmt.mappings().all()

    @classmethod
    async def ensure_default_point(cls):
        """
        Ensure that a Points object with id=1, region_id=None, addres="БЕЗ ПУНКТА" exists in the database.
        If not, create it.
        """
        async with async_session_maker() as session:
            result = await session.execute(
                select(Points).where(
                    Points.id == 1,
                    Points.region_id == None,
                    Points.addres == "БЕЗ ПУНКТА",
                )
            )
            point = result.scalars().first()
            if not point:
                stmt = insert(Points).values(id=1, region_id=None, addres="БЕЗ ПУНКТА")
                await session.execute(stmt)
                await session.commit()
