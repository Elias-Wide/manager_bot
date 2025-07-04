"""Filters for handling user-related checks in the bot."""

import os
from aiogram.filters import BaseFilter
from aiogram.types import Message

from app.bot.utils import download_file_from_bot, generate_filename
from app.core.config import REPORTS_DIR, settings
from app.core.constants import FMT_JPG
from app.points.dao import PointsDAO
from app.points.models import Points
from app.users.dao import UsersDAO
from app.users.models import Users


class ObjectExistFilter(BaseFilter):
    """
    Base filter to check if an object exists in the database by a given attribute.

    Args:
        modelDAO: Data access object for the model.
        attr_name: Attribute name to filter by.

    Returns:
        dict: Dictionary with attribute and model object if found.
        bool: False if object does not exist.
    """

    def init(self, modelDAO: UsersDAO | PointsDAO, attr_name: str) -> None:
        self.modelDAO = modelDAO
        self.attr_name: str = attr_name

    async def __call__(
        self,
        attr_name: str,
        attr_value: int,
    ) -> bool | dict[str]:
        """
        Check if an object exists in the database by attribute.

        Args:
            attr_name (str): Attribute name.
            attr_value (int): Attribute value.

        Returns:
            dict: Object data if found, otherwise False.
        """
        obj = await self.modelDAO.get_by_attribute(
            attr_name=attr_name, attr_value=attr_value
        )
        if obj:
            return {"model_obj": obj}
        return False


class UserExistFilter(ObjectExistFilter):
    """
    Filter class to check if a user exists based on their Telegram ID.

    Returns:
        bool: True for a registered user, otherwise False.
    """

    def __init__(self) -> None:
        self.modelDAO = UsersDAO
        self.attr_name = "telegram_id"

    async def __call__(
        self,
        message: Message,
    ) -> bool:
        """
        Check if the user exists in the database.

        Args:
            message (Message): The incoming message object.

        Returns:
            bool: True if the user exists, otherwise False.
        """
        attr_value = message.from_user.id
        is_user_exist: dict = await super().__call__(self.attr_name, attr_value)
        if is_user_exist:
            return {"user": is_user_exist["model_obj"]}


class BanFilter(UserExistFilter):
    """
    Filter class to check if a user is banned.

    Inherits from UserExistFilter to perform a basic registration check
    and adds a ban status check.

    Returns:
        bool: False if the user is banned, otherwise the user object.
    """

    async def __call__(self, message: Message):
        """
        Check if the user is banned.

        Args:
            message (Message): The incoming message object.

        Returns:
            bool: False if the user is banned, otherwise the user object.
        """
        is_user_exist = await super().__call__(message)
        if is_user_exist and is_user_exist["user"].ban is True:
            return False
        return is_user_exist


class RegionAdminFilter(UserExistFilter):

    async def __call__(self, message: Message):
        is_registered_user = await super().__call__(message)
        if is_registered_user:
            return is_registered_user["user"].is_region_admin


class AdminFilter(BaseFilter):
    """
    Filter class to check if the user has admin rights.

    Returns:
        bool: True if the user is the admin, otherwise False.
    """

    async def __call__(self, message: Message):
        """
        Check if the user is the admin.

        Args:
            message (Message): The incoming message object.

        Returns:
            bool: True if the user is the admin, otherwise False.
        """
        if message.from_user.id == int(settings.telegram.admin_id):
            return True
        return False


class NameValidationFilter(BaseFilter):
    """
    Filter class to validate the format of a user's name and surname.

    Returns:
        dict: Dictionary with first_name and last_name if valid, otherwise False.
    """

    async def __call__(self, message: Message) -> bool:
        """
        Validate the name format in the message.

        Args:
            message (Message): The incoming message object.

        Returns:
            dict: Dictionary with first_name and last_name if valid, otherwise False.
        """
        if not message.text or len(message.text.split()) != 2:
            return False
        first_name, last_name = message.text.split()
        if not (first_name.isalpha() and last_name.isalpha()):
            return False
        return {"first_name": first_name, "last_name": last_name}


class PointExistFilter(ObjectExistFilter):
    """
    Filter class to check if a point exists based on its ID.

    Returns:
        bool: True if the point exists, otherwise False.
    """

    def __init__(self) -> None:
        self.modelDAO = PointsDAO
        self.attr_name = "id"

    async def __call__(self, message: Message) -> bool:
        """
        Check if the point exists in the database.

        Args:
            message (Message): The incoming message object.

        Returns:
            bool: True if the point exists, otherwise False.
        """
        attr_value = int(message.text)
        is_point_exist = await super().__call__(self.attr_name, attr_value)
        if is_point_exist:
            return {"point": is_point_exist["model_obj"]}


class RegionPointFilter(PointExistFilter):
    """
    Filter class to check if the point belongs to the same region as the user.

    Returns:
        bool: True if the point's region matches the user's region, otherwise False.
    """

    async def __call__(self, message):
        """
        Check if the point's region matches the user's region.

        Args:
            message (Message): The incoming message object.

        Returns:
            bool: True if the regions match, otherwise False.
        """

        point: dict[str:Points] = await super().__call__(message)
        if not point:
            return False
        user: Users = await UsersDAO.get_by_attribute(
            attr_name="telegram_id", attr_value=message.from_user.id
        )
        return point if point["point"].region_id == user.region_id else False


class ValidatePhotoFilter(BaseFilter):
    """
    Filter class to validate and save a photo from the message buffer.

    Downloads the photo, saves it to the reports directory, and returns the image name.

    Returns:
        dict: Dictionary with the saved image name.
    """

    async def __call__(self, message: Message):
        """
        Download the photo from the message buffer and save it to the reports directory.

        Args:
            message (Message): The incoming message object.

        Returns:
            dict: Dictionary with the saved image name.
        """
        img_in_buffer = await download_file_from_bot(message)
        img_name: str = await generate_filename()
        file_path = os.path.join(REPORTS_DIR, img_name + FMT_JPG)
        with open(file_path, "wb") as f:
            f.write(img_in_buffer.getbuffer())
        return {"img_name": img_name}
