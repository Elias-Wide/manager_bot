from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import ContentType, Message

from app.bot.filters import AdminFilter
from app.bot.states import AdminStates
from app.bot.utils import read_excel_file
from app.offices.dao import OfficesDAO

admin_router = Router()
admin_router.message.filter(AdminFilter())


@admin_router.message(Command("d_offices"))
async def procces_dnwld_office_command(message: Message, state: FSMContext):
    """Prompts the user to upload a file with offices data."""
    await message.answer(text="Загрузите необходимый файл.")
    await state.set_state(AdminStates.dwnld_offices)


@admin_router.message(
    AdminStates.dwnld_offices, F.content_type == ContentType.DOCUMENT
)
async def proccess_dwnld_file(message: Message, state: FSMContext):
    """Processes the uploaded file and saves office data to the database."""
    office_list = await read_excel_file(message=message)
    for office_data in office_list:
        await OfficesDAO.create(office_data)
    await message.answer(text="Success!")
