from app.offices.models import Offices
from app.reports.models import Reports
from app.users.dao import UsersDAO
from app.users.models import Users


class Captions:
    no_caption: str = ""
    choose_office: str = "Введите id пункта."
    bot_first_message: str = (
        "Привет! Я бот для менеджеров ВБ. Чтобы начать, мне нужно немного "
        "информации о тебе."
    )
    name_question: str = "Укажите ваше имя и фамилию в формате 'Имя Фамилия'."
    incorrect_name_format: str = (
        "Некорректный формат имени. Пожалуйста, укажите имя и фамилию в формате "
        "'Имя Фамилия'."
    )
    reports_menu: str = "Отправить отчет прихода 📨"
    incorrect_phone_number: str = "Неверный формат номера."
    phone_number_question: str = "Укажите ваш номер телефона в формате +7XXXXXXXXXX."
    office_id_question: str = (
        "Укажите ID пункта, в котором вы работаете.\n"
        "Если нет постоянного пункта - отправьте 1."
    )
    office_not_in_region: str = "Пункт не относится к Вашему региону."
    incorrect_office_id: str = (
        "Пункт с таким ID не найден. Пожалуйста, проверьте введенный ID и "
        "попробуйте снова."
    )
    no_reports_today: str = "На сегодня отчетов нет."
    incorrect_office_id_format: str = "ID должен быть числом"
    report_created_today: str = "❕Отчет для {addres} на сегодня уже отправлен❕"
    reports_incorrect_photo_format: str = "❌Пожалуйста, отправьте фото для отчета.❌"
    reports_success: str = "✅Отчет успешно отправлен✅"
    send_photo: str = "Пункт {addres} iD {office_id}\n\n" "Загрузите фото для отчета."

    def __getattr__(self, name):
        """
        Return a default caption if the requested attribute does not exist.

        Args:
            name (str): The name of the requested attribute.

        Returns:
            str: The default caption.
        """
        return self.no_caption

    async def get_office_report_caption(self, report: Reports) -> str:
        return (
            f"{report["addres"]}  iD {report.office_id}\n"
            f"{report.created_at.strftime("%d.%m.%Y %H:%M")}\n"
            f"Менеджер {report["first_name"]} {report["last_name"]} "
            f" @{report["username"]}\n"
        )

    async def get_office_info(self, office: Offices, managers: list[Users]) -> str:
        result_str: str = office.get_full_info()
        working_managers_id: Users = tuple(
            m.id for m in (await UsersDAO.get_workday_manager(office.id))
        )
        if managers:
            for manager in managers:
                manager_info = manager.get_full_info()
                result_str += (
                    "📍НА СМЕНЕ📍\n" + manager_info + "\n\n"
                    if manager.id in working_managers_id
                    else manager_info + "\n\n"
                )
            return result_str
        return result_str + "❗️На пункте нет постоянных менеджеров❗️"


async def get_user_full_data(user_id: int) -> str:
    """
    Get full user data as a formatted string.

    Args:
        user_id (int): Telegram user ID.

    Returns:
        str: Formatted user data or error message.
    """
    try:
        user: Users = await UsersDAO.get_user_full_data(user_id)
        result = (
            f"Ваши данные 📂: \n\n"
            f"{user.last_name} {user.first_name}\n"
            f"Юзернэйм 📱:    {user.username}\n"
            f"Адрес пункта 🏚:    {user.addres}\n"
        )
        return (
            result + f"ID пункта: {user.office_id} 📌\n"
            if user.office_id != 1
            else result
        )
    except Exception as error:
        print(error)
        return "Ошибка получения данных"


captions = Captions()
