"""
Модуль констант для текста и колбэкдата кнопок.
Сначала идут "простые" константы в алфавитном порядке,
потом сложные - dict, tuple.
"""

ALL_PHOTOS: str = "all_photos"
CRITICAL_ERROR: str = "Критическая ошибка. Перезапустите бота."
BACK_BTN: str = "Назад ◀️"
CANCEL: str = "cancel"
CONFIRM_SCHEDULE: str = "confirm_schedule"
CONFIRM_SEND: str = "confirm_send"
CHOOSE_OFFICE: str = "choose_office"
GET_DAY_REPORT: str = "day_report"
GET_OFFICE_MANAGERS: str = "get_office_info"
GET_OFFICE_REPORT: str = "get_office_report"
GET_REGION_SCHEDULE: str = "region_schedule"
EMPTY_BTN: str = "Это пустые кнопки, не балуйся!"
NONE_MENU: str = "none"
CHANGE_MONTH: str = "change_month"
MAIN_MENU: str = "main_menu"
MY_OFFICE_REPORT: str = "my_office_report"
OTHER_OFFICE_REPORT: str = "other_office_report"
PROFILE_MENU: str = "profile_menu"
REPORT: str = "report"
REPORTS_MENU: str = "reports_menu"
SET_SCHEDULE: str = "set_schedule"
SCHEDULE: str = "schedule"

CONFIRM_REGISTRATION: dict[str, str] = {
    "confirm": "Зарегистрироваться✅",
}
CONFIRM_SCHEDULE_BTN: tuple[str] = (CONFIRM_SCHEDULE, "Сохранить график 📝")
CALENDAR_BTNS: tuple[tuple[str]] = tuple(
    (NONE_MENU, text) for text in ("ПН", "ВТ", "СР", "ЧТ", "ПТ", "СБ", "ВС")
)
MAIN_MENU_COMMANDS: dict[str] = {
    "/start": "Перезапуск бота/открыть меню",
    "/get_work": "Отчет прихода на свой пункт",
}

MAIN_MENU_BUTTONS: tuple[tuple[str]] = (
    (PROFILE_MENU, "Профиль 📋"),
    (REPORTS_MENU, "Отчет прихода 📨"),
)
MAIN_MENU_PAGES: tuple[str] = (MAIN_MENU, PROFILE_MENU, REPORTS_MENU)
PROFILE_MENU_BTNS: tuple[tuple[str]] = ((SCHEDULE, "График работы 🗓"),)
REPORTS_MENU_BTNS: tuple[tuple[str]] = (
    (MY_OFFICE_REPORT, "Мой пункт 📍"),
    (OTHER_OFFICE_REPORT, "На замене"),
)
REPORTS_MENU_BTNS_MINI: tuple[tuple[str]] = (REPORTS_MENU_BTNS[1],)
WB_ADMIN_MENU_PAGES: tuple[str] = (
    ALL_PHOTOS,
    GET_OFFICE_REPORT,
    GET_DAY_REPORT,
    GET_OFFICE_MANAGERS,
    GET_REGION_SCHEDULE,
)
WB_ADMIN_MENU_BTNS: tuple[tuple[str]] = (
    (ALL_PHOTOS, "Все отчеты прихода 📸"),
    (GET_OFFICE_REPORT, "Отчет по id пункта 🏢"),
    (GET_DAY_REPORT, "Общий отчет по региону 📝"),
    (GET_OFFICE_MANAGERS, "Контакты пункта 📱"),
    (GET_REGION_SCHEDULE, "График менеджеров 📆"),
)
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
