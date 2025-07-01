import os
import re
import random
import string
from io import BytesIO
from aiogram.types import ContentType, Message
import openpyxl

from app.core.constants import (
    FMT_JPG,
)
from app.bot.init_bot import bot


async def generate_filename() -> str:
    filename = [
        random.choice(
            string.ascii_lowercase + string.digits if i != 5 else string.ascii_uppercase
        )
        for i in range(10)
    ]
    return "".join(filename)


async def is_file_in_dir(name, path) -> None:
    for root, dirs, files in os.walk(path):
        if name in files:
            return True
        return False


async def delete_file(path: str, file_name: str):
    """Delete a file in the specified directory."""
    try:
        os.remove(path / (file_name + FMT_JPG))
    except:
        print("Error deleting file")


async def delete_files_in_folder(folder_path: str):
    """Delete all files in the specified directory."""
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"Error deleting file {file_path}. {e}")


async def download_file(file, destination) -> str:
    """
    Download a file.
    A name is generated, the file is downloaded from the bot and
    saved in the specified directory.
    """
    file_name = await generate_filename()
    filename_with_format = file_name + FMT_JPG
    path = destination / (file_name + FMT_JPG)
    file_from_bot = await bot.get_file(file.file_id)
    destination_file = await bot.download_file(
        file_from_bot.file_path, os.path.join(os.getcwd(), path)
    )
    return file_name


async def get_image(filename: str):
    """Get the required file by name."""
    pass


async def delete_file(path: str):
    """Delete a file in the specified directory."""
    try:
        os.remove(path)
    except:
        print("Error deleting file")


async def read_excel_file(message: Message):
    """Process data from an Excel file with office data."""

    xlsx_file_in_buffer = await download_file_from_bot(message)
    workbook = openpyxl.load_workbook(xlsx_file_in_buffer)
    sheet = workbook.active
    return [
        {
            "id": row[0],
            "addres": row[1],
            "name": row[3],
        }
        for row in sheet.iter_rows(values_only=True)
    ]


async def download_file_from_bot(message: Message) -> BytesIO:
    """Загрузка файла из бота в буфер."""

    buffer = BytesIO()
    if message.content_type == ContentType.PHOTO:
        file_from_bot = await bot.get_file(message.photo[-1].file_id)
    elif message.content_type == ContentType.DOCUMENT:
        file_from_bot = await bot.get_file(message.document.file_id)
    return await bot.download_file(file_from_bot.file_path, buffer)
