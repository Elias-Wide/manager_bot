from datetime import datetime
from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery, Message


from app.bot.filters import PointExistFilter
from app.bot.handlers.callbacks.main_menu import (
    get_menu,
    procces_main_menu_comand,
)
from app.bot.keyboards.banners import get_img
from app.bot.keyboards.buttons import (
    CHOOSE_OFFICE,
    CONFIRM_SCHEDULE,
    CRITICAL_ERROR,
    EMPTY_BTN,
    MAIN_MENU_PAGES,
    NONE_MENU,
    OTHER_OFFICE_REPORT,
    PROFILE_MENU,
    REPORTS_MENU,
    SCHEDULE,
)
from app.bot.keyboards.calendar_kb import get_days_btns
from app.bot.keyboards.main_kb_builder import MenuCallBack, get_btns
from app.bot.states import ProfileStates, ReportsStates
from app.core.constants import DATE_FORMAT
from app.points.models import Points
from app.users.dao import UsersDAO, WorkDaysDAO
from app.users.models import Users


user_router = Router()


@user_router.message(CommandStart())
async def process_start_command(
    message: Message,
    state: FSMContext,
) -> None:
    """После завершения анкетирования. Начало самого бота."""
    await procces_main_menu_comand(message)
    await state.clear()


@user_router.callback_query(MenuCallBack.filter(F.menu_name.in_(MAIN_MENU_PAGES)))
async def user_menu(
    callback: CallbackQuery, callback_data: MenuCallBack, state: FSMContext
) -> None:
    """Обработка нажатия кнопок меню."""
    await state.clear()
    try:
        await get_menu(callback, callback_data)
        await callback.answer()
    except Exception as error:
        print(error)
        await callback.answer(
            text="Критическая ошибка / перезапустите бота", show_alert=True
        )


@user_router.callback_query(
    MenuCallBack.filter(
        F.menu_name.in_(
            SCHEDULE,
        )
    ),
    default_state,
)
async def set_user_schedule(
    callback: CallbackQuery, callback_data: MenuCallBack, state: FSMContext
) -> None:
    try:
        user: Users = await UsersDAO.get_by_attribute(
            attr_name="telegram_id", attr_value=callback.from_user.id
        )
        callback_data.user_id = user.id
        user_schedule = [
            w_day.day
            for w_day in await WorkDaysDAO.get_user_working_days(
                user_id=callback_data.user_id
            )
        ]
        await callback.message.edit_media(
            media=await get_img(SCHEDULE),
            reply_markup=await get_days_btns(
                user_id=callback_data.user_id,
                level=callback_data.level,
                user_schedule=user_schedule.copy(),
            ),
        )
        await state.update_data(user_id=user.id, user_schedule=sorted(user_schedule))
        await state.set_state(ProfileStates.set_schedule)
    except Exception as error:
        print(error)
        await callback.answer(text=CRITICAL_ERROR, show_alert=True)


@user_router.callback_query(
    ProfileStates.set_schedule,
    MenuCallBack.filter(F.menu_name.in_((SCHEDULE, CONFIRM_SCHEDULE))),
)
async def procce_set_schedule(
    callback: CallbackQuery, callback_data: MenuCallBack, state: FSMContext
):
    """Обработка нажатий кнопок календаря."""
    user = await UsersDAO.get_by_attribute(
        attr_name="telegram_id", attr_value=callback.from_user.id
    )
    await state.update_data(user_id=user.id)
    state_data = await state.get_data()
    user_schedule = state_data["user_schedule"]
    print(user_schedule)
    if callback_data.menu_name == CONFIRM_SCHEDULE:
        print(state_data["user_schedule"])
        try:
            await WorkDaysDAO.set_user_schedule(
                user_id=user.id, work_days=user_schedule
            )
            await state.clear()
            await callback.answer(text="График успешно сохранен.")
            callback_data.level, callback_data.menu_name = 1, PROFILE_MENU
            await get_menu(callback, callback_data)
        except Exception as error:
            print("CONFIRM_SCHEDULE ERROR", error)
            await callback.answer(text=CRITICAL_ERROR, show_alert=True)
    else:
        if callback_data.day:
            date = datetime.strptime(callback_data.day, DATE_FORMAT).date()
            if date in user_schedule:
                user_schedule.remove(date)
            else:
                user_schedule.append(
                    datetime.strptime(callback_data.day, DATE_FORMAT).date()
                )
                user_schedule = sorted(user_schedule)
                print(user_schedule)
            await callback.message.edit_media(
                media=await get_img(SCHEDULE),
                reply_markup=await get_days_btns(
                    user_id=callback_data.user_id,
                    level=callback_data.level,
                    user_schedule=user_schedule.copy(),
                ),
            )
        else:
            await callback.answer()


@user_router.callback_query(
    ProfileStates.set_schedule,
    MenuCallBack.filter(
        F.menu_name.in_(
            NONE_MENU,
        )
    ),
)
async def proccess_empty_btn(
    callback: CallbackQuery, callback_data: MenuCallBack, state: FSMContext
) -> None:
    """Обработка нажатий пустых кнопок с днями недели в календаре."""
    await callback.answer(text=EMPTY_BTN)
    await procce_set_schedule(callback, callback_data, state)


@user_router.callback_query(
    MenuCallBack.filter(
        F.menu_name.in_(
            OTHER_OFFICE_REPORT,
        )
    ),
    default_state,
)
async def choose_office(
    callback: CallbackQuery,
    callback_data: MenuCallBack,
    state: FSMContext,
) -> None:
    """
    Обработка нажатия кнопки выбора офиса для отчета.
    Переход к следующему состоянию для выбора офиса.
    """
    await state.set_state(ReportsStates.choose_office)
    await callback.message.edit_media(
        media=await get_img(CHOOSE_OFFICE),
        reply_markup=await get_btns(
            menu_name=REPORTS_MENU,
            previous_menu=REPORTS_MENU,
            level=2,
            need_back_btn=True,
        ),
    )


@user_router.message(ReportsStates.choose_office, F.text.isdigit(), PointExistFilter())
async def send_report_photo(
    message: Message, state: FSMContext, model_obj: Points
) -> None:
    """
    Обработка ввода ID офиса для отчета.
    Переход к следующему состоянию для отправки фото отчета.
    """
    point_id = int(message.text)
    btn_text = (
        f"Пункт {model_obj.addres} iD{model_obj.id}\n\n" f"Загрузите фото для отчета."
    )
    await state.update_data(point_id=point_id)
    await state.set_state(ReportsStates.send_photo)
    await message.answer(text=btn_text)


@user_router.message(ReportsStates.choose_office, F.text.isdigit(), ~PointExistFilter())
async def incorrect_office_id_handler(message: Message, state: FSMContext) -> None:
    """
    Обработка некорректного ввода ID офиса.
    Отправка сообщения об ошибке.
    """
    await message.answer(text="Пункт отсутствует в бд.")


@user_router.message(ReportsStates.choose_office, ~F.text.isdigit())
async def incorrect_office_id_format_handler(
    message: Message, state: FSMContext
) -> None:
    """
    Обработка некорректного формата ID офиса.
    Отправка сообщения об ошибке.
    """
    await message.answer(text="ID  офиса должен быть числом.")


@user_router.message(ReportsStates.send_photo, F.photo)
async def send_report_photo_handler(
    message: Message,
    state: FSMContext,
) -> None:
    """
    Обработка отправки фото отчета.
    Сохранение фото и переход к следующему состоянию.
    """
    user_data = await state.get_data()
    point_id = user_data.get("point_id")
    photo = message.photo[-1]
    try:
        # await UsersDAO.save_report_photo(
        #     user_id=message.from_user.id,
        #     point_id=point_id,
        #     photo=photo.file_id
        # )
        await message.answer(text="Фото успешно отправлено!")
        await state.clear()
    except Exception as error:
        print(error)
        await message.answer(text=CRITICAL_ERROR, show_alert=True)


@user_router.message(ReportsStates.send_photo, ~F.photo)
async def incorrect_photo_handler(
    message: Message,
    state: FSMContext,
) -> None:
    """
    Обработка некорректного формата фото отчета.
    Отправка сообщения об ошибке.
    """
    await message.answer(text="Отправьте фото для отчета.")
