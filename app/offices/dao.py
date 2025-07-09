from sqlalchemy import and_, func, insert, select
from app.dao.base import BaseDAO
from app.core.database import async_session_maker
from app.offices.constants import NO_OFFICE_ADDRES, NO_OFFICE_ID
from app.offices.models import Offices


class OfficesDAO(BaseDAO):
    model = Offices

    @classmethod
    async def search_by_addres(cls, searching_address: str):
        async with async_session_maker() as session:
            stmt = await session.execute(
                select(cls.model.__table__.columns)
                .where(
                    and_(
                        func.lower(Offices.addres).contains(
                            searching_address.lower(),
                        ),
                        Offices.id != 1,
                    )
                )
                .order_by("addres")
            )
            return stmt.mappings().all()

    @classmethod
    async def get_offices_by_region_id(
        cls, region_id: int, working_schedule: str | None = None
    ):
        async with async_session_maker() as session:
            stmt = ((Offices.region_id == region_id),)
            if working_schedule:
                stmt = (
                    and_(
                        Offices.region_id == region_id,
                        Offices.working_schedule == working_schedule,
                    ),
                )
            offices = await session.execute(
                select(Offices.__table__.columns).where(*stmt)
            )
            return offices.mappings().all()

    @classmethod
    async def ensure_default_office(cls):
        """
        Ensure that a Offices object with id=1, region_id=None, addres="БЕЗ ПУНКТА" exists in the database.
        If not, create it.
        """
        async with async_session_maker() as session:
            result = await session.execute(
                select(Offices).where(
                    Offices.id == NO_OFFICE_ID,
                    Offices.region_id == None,
                    Offices.addres == NO_OFFICE_ADDRES,
                )
            )
            office = result.scalars().first()
            if not office:
                stmt = insert(Offices).values(
                    id=1, region_id=None, addres=NO_OFFICE_ADDRES
                )
                await session.execute(stmt)
                await session.commit()
