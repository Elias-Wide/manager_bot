from aiogram.types import FSInputFile, InputMediaPhoto

from app.bot.keyboards.buttons import NO_IMAGE
from app.bot.keyboards.captions import captions
from app.bot.utils import is_file_in_dir
from app.core.config import STATIC_DIR
from app.core.constants import FMT_JPG


BANNERS_DIR = STATIC_DIR / "banners"


async def get_img(
    menu_name: str,
    file_dir: str = BANNERS_DIR,
    f_type: str = FMT_JPG,
) -> InputMediaPhoto:
    """
    Get an image with a caption.
    The function receives the menu name and description.
    If there is no description, it is taken from the Captions class.
    If the required image is not found, the 'no_image' picture is used.
    """
    media = await get_file(menu_name, file_dir, f_type)
    return InputMediaPhoto(
        media=await get_file(menu_name, file_dir, f_type),
        caption=getattr(captions, menu_name),
    )


async def get_file(
    filename: str, file_dir: str = BANNERS_DIR, f_type: str = FMT_JPG
) -> FSInputFile:
    """
    Get a file of type FSInputFile by name in the specified directory.
    """
    if await is_file_in_dir(filename + f_type, file_dir):
        return FSInputFile(file_dir.joinpath(filename + f_type))
    return FSInputFile(file_dir.joinpath(NO_IMAGE + FMT_JPG))
