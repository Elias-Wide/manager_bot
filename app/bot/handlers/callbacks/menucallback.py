from aiogram.filters.callback_data import CallbackData


class MenuCallBack(CallbackData, prefix="menu"):
    """
    A callback data class for handling menu-related interactions in the bot.

    Attributes:
        level (int): The level of the menu hierarchy. Defaults to 0.
        menu_name (str): The name of the menu being interacted with.
        user_id (int | None): The ID of the user interacting with the menu.
                              Defaults to None if not provided.
    """

    level: int = 0
    user_id: int | None = None
    day: str | None = None
    region_id: int | None = None
    menu_name: str


class RegionAdminCallBack(MenuCallBack, prefix="wb_admin"):

    region_id: int
