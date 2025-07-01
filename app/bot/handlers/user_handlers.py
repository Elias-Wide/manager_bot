from datetime import datetime
from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery, Message


from app.bot.handlers.callbacks.main_menu import (
    get_menu,
    procces_main_menu_comand,
)
from app.bot.keyboards.banners import get_img
from app.bot.keyboards.buttons import (
    CONFIRM_SCHEDULE,
    CRITICAL_ERROR,
    EMPTY_BTN,
    MAIN_MENU_PAGES,
    NONE_MENU,
    PROFILE_MENU,
    SCHEDULE,
)
from app.bot.keyboards.calendar_kb import get_days_btns
from app.bot.keyboards.main_kb_builder import MenuCallBack
from app.bot.states import ProfileStates
from app.core.constants import DATE_FORMAT
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
        user_schedule = await WorkDaysDAO.get_user_working_days(user_id=user.id)
        print(user_schedule)
        await callback.message.edit_media(
            media=await get_img(SCHEDULE),
            reply_markup=await get_days_btns(
                user_id=callback_data.user_id,
                level=callback_data.level,
                user_schedule=user_schedule.copy(),
            ),
        )
        # await state.update_data(user_id=user.id)
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
    state_data = await state.get_data()
    user_schedule = state_data["user_schedule"]
    print(user_schedule)
    if callback_data.menu_name == CONFIRM_SCHEDULE:
        print(state_data["user_schedule"])
        try:
            # await WorkDaysDAO.set_user_schedule(
            #     user_id=state_data["user_id"],
            #     work_days=user_schedule
            # )
            await state.clear()
            await callback.answer(
                text="График успешно сохранен. Не забудьте включить уведомления по графику."
            )
            callback_data.level, callback_data.menu_name = 1, PROFILE_MENU
            await get_menu(callback, callback_data)
        except:
            print("CONFIRM_SCHEDULE ERROR")
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
