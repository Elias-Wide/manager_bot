"""Модуль с функциями анкеты."""

from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import (
    CallbackQuery,
    Message,
)

from app.bot.filters import (
    NameValidationFilter,
    PointExistFilter,
    UserExistFilter,
)
from app.bot.keyboards.registration_kb import create_registration_kb
from app.bot.keyboards.captions import Captions
from app.bot.lexicon import RegistrationQuestions
from app.bot.states import RegistrationStates
from app.users.dao import UsersDAO


registration_router = Router()
registration_router.message.filter(~UserExistFilter())


@registration_router.message(default_state, CommandStart())
async def begin_registration(
    message: Message,
    state: FSMContext,
) -> None:
    await message.answer(
        Captions.bot_first_message,
        reply_markup=await create_registration_kb(),
    )
    await state.set_state(RegistrationStates.consent_confirm)


@registration_router.callback_query(
    RegistrationStates.consent_confirm, F.data == "confirm"
)
async def name_question(
    callback: CallbackQuery,
    state: FSMContext,
) -> None:
    await callback.message.answer(text=Captions.name_question)
    await state.set_state(RegistrationStates.name_question)


@registration_router.message(
    RegistrationStates.name_question,
    F.content_type == "text",
    ~NameValidationFilter(),
)
async def name_question_error(
    message: Message,
) -> None:
    await message.answer(text=Captions.incorrect_name_format)


@registration_router.message(
    RegistrationStates.name_question,
    F.content_type == "text",
    NameValidationFilter(),
)
async def phone_number_question(
    message: Message, state: FSMContext, first_name: str, last_name: str
) -> None:
    await state.update_data(first_name=first_name, last_name=last_name)
    await message.answer(text=Captions.phone_number_question)
    await state.set_state(RegistrationStates.phone_number_question)


@registration_router.message(
    RegistrationStates.phone_number_question,
    F.content_type == "text",
    ~F.text.regexp(r"^\+7\d{10}$"),
)
async def phone_number_question_error(message: Message) -> None:
    await message.answer(text=Captions.incorrect_phone_number)


@registration_router.message(
    RegistrationStates.phone_number_question,
    F.content_type == "text",
    F.text.regexp(r"^\+7\d{10}$"),
)
async def ask_point_id_question(
    message: Message,
    state: FSMContext,
) -> None:
    await state.update_data(phone_number=message.text.strip())
    await message.answer(text=Captions.point_id_question)
    await state.set_state(RegistrationStates.point_id_question)


@registration_router.message(
    RegistrationStates.point_id_question,
    F.text.is_digit(),
    ~PointExistFilter(),
)
async def point_id_question_error(
    message: Message,
) -> None:
    await message.answer(
        text=Captions.incorrect_point_id,
    )


@registration_router.message(
    RegistrationStates.point_id_question,
    ~F.text.is_digit(),
)
async def point_id_question_error(
    message: Message,
) -> None:
    await message.answer(
        text=Captions.incorrect_point_id_format,
    )


@registration_router.message(
    RegistrationStates.point_id_question,
    F.text.is_digit(),
    PointExistFilter(),
)
async def finish_registration(
    message: Message,
    state: FSMContext,
    point_id: int,
) -> None:
    data = await state.get_data()
    await UsersDAO.create(
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        first_name=data["first_name"],
        last_name=data["last_name"],
        phone_number=data["phone_number"],
        point_id=point_id,
    )
    await state.clear()
