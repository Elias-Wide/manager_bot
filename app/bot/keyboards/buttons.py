"""
Модуль констант для текста и колбэкдата кнопок.
Сначала идут "простые" константы в алфавитном порядке,
потом сложные - dict, tuple.
"""

CRITICAL_ERROR: str = "Критическая ошибка. Перезапустите бота."
BACK_BTN: str = "Назад ◀️"
CANCEL: str = "cancel"
CONFIRM_SCHEDULE: str = "confirm_schedule"
CONFIRM_SEND: str = "confirm_send"
EMPTY_BTN: str = "Это пустые кнопки, не балуйся!"
NONE_MENU = "none"
MAIN_MENU: str = "main_menu"

PROFILE_MENU: str = "profile_menu"
REPORT: str = "report"
SET_SCHEDULE: str = "set_schedule"
SEND_QR: str = "qr_send"
SCHEDULE: str = "schedule"
UPDATE_QR: str = "qr_update"

CONFIRM_REGISTRATION: dict[str, str] = {
    "confirm": "Зарегистрироваться✅",
}
CONFIRM_SCHEDULE_BTN: tuple[str] = (CONFIRM_SCHEDULE, "Сохранить график 📝")
CALENDAR_BTNS: tuple[tuple[str]] = tuple(
    (NONE_MENU, text) for text in ("ПН", "ВТ", "СР", "ЧТ", "ПТ", "СБ", "ВС")
)
MAIN_MENU_COMMANDS: dict[str] = {
    "/start": "Перезапуск бота/открыть меню",
    "/profile": "Меню профиля",
    "/report": "Отчет прихода",
}

MAIN_MENU_BUTTONS: tuple[tuple[str]] = (
    (PROFILE_MENU, "Профиль 📋"),
    (REPORT, "Отчет прихода 📨"),
)
MAIN_MENU_PAGES: tuple[str] = (
    MAIN_MENU,
    PROFILE_MENU,
)
PROFILE_MENU_BTNS: tuple[tuple[str]] = ((SCHEDULE, "График работы 🗓"),)


# IMAGES
NO_IMAGE: str = "no_image"

# CALENDAR
DAY: dict[int, str] = {
    0: "пн",
    1: "вт",
    2: "ср",
    3: "чт",
    4: "пт",
    5: "сб",
    6: "вс",
}
MONTH: dict[int, str] = {
    1: "Январь",
    2: "Февраль",
    3: "Март",
    4: "Апрель",
    5: "Май",
    6: "Июнь",
    7: "Июль",
    8: "Август",
    9: "Сентябрь",
    10: "Октябрь",
    11: "Ноябрь",
    12: "Декабрь",
}
