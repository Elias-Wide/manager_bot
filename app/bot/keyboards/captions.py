from app.reports.models import Reports
from app.users.dao import UsersDAO
from app.users.models import Users


class Captions:
    no_caption: str = ""
    choose_office: str = "Введите id пункта. Если нет постоянного - введите 1"
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
    point_id_question: str = "Укажите ID пункта, в котором вы работаете."
    incorrect_point_id: str = (
        "Пункт с таким ID не найден. Пожалуйста, проверьте введенный ID и "
        "попробуйте снова."
    )
    incorrect_point_id_format: str = "ID должен быть числом"
    report_created_today = "❕Отчет для {addres} на сегодня уже отправлен❕"
    reports_incorrect_photo_format: str = "❌Пожалуйста, отправьте фото для отчета.❌"
    reports_success: str = "✅Отчет успешно отправлен✅"
    send_photo: str = "Пункт {addres} iD {point_id}\n\n" "Загрузите фото для отчета."

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
        workday_data = await UsersDAO.get_workday_manager(5411)
        print(workday_data)
        return (
            f"{report["addres"]}  iD {report.point_id}\n"
            f"{report.created_at}\n"
            f"Менеджер {report["first_name"]} {report["last_name"]} "
            f" @{report["username"]}\n"
        )


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
            result + f"ID пункта: {user.point_id} 📌\n"
            if user.point_id != 1
            else result
        )
    except Exception as error:
        print(error)
        return "Ошибка получения данных"


captions = Captions()
