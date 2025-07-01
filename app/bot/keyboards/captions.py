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
    point_id_question: str = "Укажите ID пункта, в котором вы работаете."
    incorrect_point_id: str = (
        "Пункт с таким ID не найден. Пожалуйста, проверьте введенный ID и "
        "попробуйте снова."
    )
    incorrect_point_id_format: str = "ID должен быть числом"

    def __getattr__(self, name):
        """
        Return a default caption if the requested attribute does not exist.

        Args:
            name (str): The name of the requested attribute.

        Returns:
            str: The default caption.
        """
        return self.no_caption


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
            f"ID пункта 📌:    {user.point_id}\n"
            f"Адрес пункта 🏚:    {user.addres}\n"
        )
        return result
    except Exception as error:
        print(error)
        return "Ошибка получения данных"


captions = Captions()
