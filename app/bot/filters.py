"""Filters for handling user-related checks in the bot."""

import os
from aiogram.filters import BaseFilter
from aiogram.types import Message

from app.bot.utils import download_file_from_bot, generate_filename
from app.core.config import REPORTS_DIR, settings
from app.core.constants import FMT_JPG
from app.points.dao import PointsDAO
from app.users.dao import UsersDAO


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
            return {self.attr_name: attr_value, "model_obj": obj}
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
        return await super().__call__(self.attr_name, attr_value)


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
        user = await super().__call__(message)
        if user and user["model_obj"].ban is True:
            return False
        return user


class RegionAdminFilter(UserExistFilter):

    async def __call__(self, message: Message):
        is_registered_user = await super().__call__(message)
        if is_registered_user:
            return is_registered_user["model_obj"].is_region_admin


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
        return await super().__call__(self.attr_name, attr_value)


class ValidatePhotoFilter(BaseFilter):

    async def __call__(self, message: Message):
        img_in_buffer = await download_file_from_bot(message)
        img_name: str = await generate_filename()
        file_path = os.path.join(REPORTS_DIR, img_name + FMT_JPG)
        with open(file_path, "wb") as f:
            f.write(img_in_buffer.getbuffer())
        return {"img_name": img_name}
