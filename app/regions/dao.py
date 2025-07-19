from typing import List

from cachetools import TTLCache
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.core.database import async_session_maker
from app.dao.base import BaseDAO
from app.regions.models import Regions


class RegionsDAO(BaseDAO):
    """
    A class for CRUD operations with regions.

    This class provides methods for interacting with the `Regions` model.
    """

    model = Regions

    @classmethod
    async def get_regions_with_admins(cls) -> List[Regions]:
        """
        Get all regions with their associated admins.

        Returns:
            List[Regions]: A list of regions with their admins.
        """
        async with async_session_maker() as session:
            regions = await session.execute(
                select(cls.model).options(joinedload(cls.model.admins))
            )
            return regions.unique().scalars().all()
