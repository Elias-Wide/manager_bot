from app.dao.base import BaseDAO
from app.core.database import async_session_maker
from app.reports.models import Reports


class ReportsDAO(BaseDAO):
    """
    A class for CRUD operations with Reports.

    This class provides methods for interacting with the `Reports` model.
    """

    model = Reports
