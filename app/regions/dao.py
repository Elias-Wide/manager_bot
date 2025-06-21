from app.dao.base import BaseDAO
from app.core.database import async_session_maker
from app.regions.models import Regions


class RegionsDAO(BaseDAO):
    """
    A class for CRUD operations with regions.

    This class provides methods for interacting with the `Regions` model.
    """

    model = Regions
