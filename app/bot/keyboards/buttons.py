"""
Модуль констант для текста и колбэкдата кнопок.
Сначала идут "простые" константы в алфавитном порядке, 
потом сложные - dict, tuple.
"""

from app.core.constants import MAIN_MENU

BACK_BTN: str = "Назад ◀️"
CANCEL: str = "cancel"
CONFIRM_SCHEDULE: str = "confirm_schedule"
CONFIRM_SEND: str = "confirm_send"
EMPTY_BTN: str = "Это пустые кнопки, не балуйся!"
NONE_MENU = "none"
PROFILE: str = "profile"
REPORT: str = "report"
SET_SCHEDULE: str = "set_schedule"
SEND_QR: str = "qr_send"
SCHEDULE: str = "schedule"
UPDATE_QR: str = "qr_update"

CONFIRM_SCHEDULE_BTN: tuple[str] = (CONFIRM_SCHEDULE, "Сохранить график 📝")
CALENDAR_BTNS: tuple[tuple[str]] = tuple(
    (NONE_MENU, text) for text in ("ПН", "ВТ", "СР", "ЧТ", "ПТ", "СБ", "ВС")
)

MAIN_MENU_BUTTONS: tuple[tuple[str]] = (
    (PROFILE, "Профиль 📋"),
    (REPORT, "Отчет прихода 📨"),
)
MAIN_MENU_PAGES: tuple[str] = (
    MAIN_MENU,
    PROFILE,
)
PROFILE_MENU_BTNS: tuple[tuple[str]] = (
    (SCHEDULE, "График работы 🗓"),
)