import calendar
import os
import random
import string
from datetime import datetime
from io import BytesIO

import openpyxl
from aiogram.types import ContentType, Message
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

from app.bot.init_bot import bot
from app.core.constants import FMT_JPG
from app.offices.models import Offices
from app.users.dao import UsersDAO, WorkDaysDAO
from app.users.models import Users


async def generate_filename() -> str:
    """
    Generate a random filename consisting of 10 characters (letters and digits).

    Returns:
        str: The generated filename.
    """
    filename = [
        random.choice(
            string.ascii_lowercase + string.digits
            if i != 5
            else string.ascii_uppercase
        )
        for i in range(10)
    ]
    return "".join(filename)


async def is_file_in_dir(name, path) -> None:
    """
    Check if a file with the given name exists in the specified directory.

    Args:
        name (str): The filename to search for.
        path (str): The directory path.

    Returns:
        bool: True if the file exists, otherwise False.
    """
    for root, dirs, files in os.walk(path):
        if name in files:
            return True
        return False


async def delete_file(path: str, file_name: str):
    """
    Delete a file with the specified name in the given directory.

    Args:
        path (str): The directory path.
        file_name (str): The name of the file to delete.
    """
    try:
        os.remove(path / (file_name + FMT_JPG))
    except:
        print("Error deleting file")


async def delete_files_in_folder(folder_path: str):
    """
    Delete all files in the specified folder.

    Args:
        folder_path (str): The path to the folder.
    """
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"Error deleting file {file_path}. {e}")


async def download_file(file, destination) -> str:
    """
    Download a file from the bot and save it to the specified directory.

    Args:
        file: The file object from Telegram.
        destination: The directory to save the file.

    Returns:
        str: The generated filename (without extension).
    """
    file_name = await generate_filename()
    filename_with_format = file_name + FMT_JPG
    path = destination / (file_name + FMT_JPG)
    file_from_bot = await bot.get_file(file.file_id)
    await bot.download_file(
        file_from_bot.file_path, os.path.join(os.getcwd(), path)
    )
    return file_name


async def delete_file(path: str):
    """
    Delete a file at the specified path.

    Args:
        path (str): The full path to the file.
    """
    try:
        os.remove(path)
    except:
        print("Error deleting file")


async def read_excel_file(message: Message):
    """
    Process data from an Excel file with office data.

    Args:
        message (Message): The incoming message containing the Excel file.

    Returns:
        list[dict]: List of dictionaries with office data.
    """

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
    """
    Download a file from the bot into a memory buffer.

    Args:
        message (Message): The incoming message containing the file.

    Returns:
        BytesIO: The buffer with the downloaded file.
    """

    buffer = BytesIO()
    if message.content_type == ContentType.PHOTO:
        file_from_bot = await bot.get_file(message.photo[-1].file_id)
    elif message.content_type == ContentType.DOCUMENT:
        file_from_bot = await bot.get_file(message.document.file_id)
    return await bot.download_file(file_from_bot.file_path, buffer)


async def create_excel_report(region_report_data: list[tuple]) -> BytesIO:
    """
    Generate an Excel report in memory from a list of tuples with office report data.

    This function creates an Excel file with the following logic:
    - Initializes a new workbook and sets the active worksheet's title to "Отчеты по офисам".
    - Adds a header row with columns: "Пункт", "ID", "Менеджер", "Отчет прихода".
    - Applies bold font and centered alignment to the header cells.
    - For each row in region_report_data:
        - If the "Менеджер" field (index 2) is a list or tuple, joins its elements with a newline character so each manager appears on a new line in the cell.
        - Appends the row to the worksheet.
        - If any cell in the row contains the value "нет отчета", the entire row is filled with a red background; otherwise, it is filled with a green background.
        - The "Менеджер" column is set to wrap text and center alignment to properly display multiple managers.
        - A thin bottom border is added to each cell in the row, except for the last row.
    - Sets custom column widths for better readability.
    - Saves the workbook to a BytesIO buffer and returns it, ready for sending as a file.

    Args:
        region_report_data (list[tuple]): List of tuples, each representing a row of office report data.

    Returns:
        BytesIO: The buffer containing the generated Excel file.
    """
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Отчеты по офисам"
    headers = ["Пункт", "ID", "Менеджер", "Отчет прихода", "График работы"]
    ws.append(headers)
    header_font = Font(bold=True)
    for col_num, _ in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col_num)
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center")
    for row_idx, row in enumerate(region_report_data, start=2):
        row = list(row)
        if isinstance(row[2], (list, tuple)):
            row[2] = "\n".join(str(m) for m in row[2])
        if row[3] == False:
            row[3] = "НЕТ ОТЧЕТА"
        ws.append(row)
        fill = (
            red_fill
            if any(cell == "НЕТ ОТЧЕТА" for cell in row)
            else green_fill
        )
        for col_idx in range(1, len(headers) + 1):
            cell = ws.cell(row=row_idx, column=col_idx)
            cell.fill = fill
            cell.alignment = Alignment(
                wrap_text=True, horizontal="center", vertical="center"
            )
        if row_idx < len(region_report_data) + 1:
            for col_idx in range(1, len(headers) + 1):
                ws.cell(row=row_idx, column=col_idx).border = thin_border

    ws.column_dimensions["A"].width = 35
    ws.column_dimensions["B"].width = 10
    ws.column_dimensions["C"].width = 25
    ws.column_dimensions["D"].width = 20
    ws.column_dimensions["D"].width = 25
    buffer = BytesIO()
    wb.save(buffer)
    buffer.seek(0)
    return buffer


async def create_region_schedule(offices: list[Offices]) -> BytesIO:
    """
    Generate an Excel file with the work schedule for all offices.

    The function creates an Excel file with the following logic:
    - Determines the current month and generates a header row with all days of the month.
    - Adds columns: "Пункт", "ID", "Менеджер", followed by one column for each day of the month.
    - For each office:
        - Adds a row for each manager, showing their work schedule for the month.
        - If there are no managers, adds a row with empty manager and fills all days with red.
        - For each manager, marks "Р" (work) with green fill if the manager works that day, or "В" (off) with red fill otherwise.
    - Adds thin borders and center alignment to all cells.
    - Sets custom column widths for better readability.
    - Saves the workbook to a BytesIO buffer and returns it.

    Args:
        offices (list[Offices]): List of office objects.

    Returns:
        BytesIO: The buffer containing the generated Excel file.
    """
    today = datetime.now()
    num_days = calendar.monthrange(today.year, today.month)[1]
    month_dates: list = tuple(
        d.strftime("%m.%d")
        for d in [
            datetime(today.year, today.month, day)
            for day in range(1, num_days + 1)
        ]
    )
    wb_headers = ("Пункт", "iD", "Менеджер")
    wb_headers = wb_headers + month_dates

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "График работы"
    ws.append(wb_headers)
    row_idx = 1
    for office in offices:
        row_idx += 1
        managers_in_ws = []
        row = [office.addres, office.id, None]
        is_office_added = False
        managers: list[Users] = await UsersDAO.get_objs_by_filter(
            office_id=office.id
        )
        w_day_dict = {}
        start_row = row_idx
        for manager in managers:
            w_day_dict[manager.id] = [
                w.day.strftime("%m.%d")
                for w in await WorkDaysDAO.get_user_working_days(
                    user_id=manager.id, month=today.month
                )
            ]
        if not managers:
            ws.append(row)
            for col_idx in range(4, len(wb_headers) + 1):
                cell = ws.cell(row=start_row, column=col_idx)
                cell.fill = red_fill
        else:
            for col_idx in range(4, len(wb_headers) + 1):
                for manager in managers:
                    if not is_office_added:
                        is_office_added = True
                        row[2] = str(manager)
                        managers_in_ws.append(manager.id)
                        ws.append(row)
                    elif manager.id not in managers_in_ws:
                        row = ["", "", str(manager)]
                        managers_in_ws.append(manager.id)
                        ws.append(row)
                    cell = ws.cell(row=start_row, column=col_idx)
                    if wb_headers[col_idx - 1] in w_day_dict[manager.id]:
                        cell.value = "Р"
                        cell.fill = green_fill
                    else:
                        cell.value = "В"
                        cell.fill = red_fill
                    start_row += 1
                start_row = row_idx
            row_idx += len(managers) - 1

    for col_idx in range(1, len(wb_headers) + 1):
        for row_idx in range(1, len(tuple(ws.iter_rows())) + 1):
            ws.cell(row=row_idx, column=col_idx).border = thin_border
            ws.cell(row=row_idx, column=col_idx).alignment = Alignment(
                horizontal="center", vertical="center"
            )
    for column_cells in ws.columns:
        ws.column_dimensions[column_cells[0].column_letter].width = 5
    ws.column_dimensions["A"].width = 35
    ws.column_dimensions["B"].width = 10
    ws.column_dimensions["C"].width = 25
    buffer = BytesIO()
    wb.save(buffer)
    buffer.seek(0)
    return buffer


thin_border = Border(
    left=Side(style="thin"),
    right=Side(style="thin"),
    top=Side(style="thin"),
    bottom=Side(style="thin"),
)
red_fill = PatternFill(
    start_color="FFC7CE", end_color="FFC7CE", fill_type="solid"
)
green_fill = PatternFill(
    start_color="00008000", end_color="00008000", fill_type="solid"
)
