from app.dao.base import BaseDAO
from app.core.database import async_session_maker
from app.reports.models import Reports


class ReportsDAO(BaseDAO):
    """
    A class for CRUD operations with Reports.

    This class provides methods for interacting with the `Reports` model.
    """

    model = Reports

    @classmethod
    async def get_reports_by_region(region_id: int) -> list[Reports] | None:
        pass
    
    
