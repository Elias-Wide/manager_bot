class RegistrationQuestions:
    BOT_FIRST_MESSAGE: str = (
        "Привет! Я бот для менеджеров ВБ. "
        "Чтобы начать, мне нужно немного информации о тебе."
    )
    NAME_QUESTION: str = "Укажите ваше имя и фамилию в формате 'Имя Фамилия'."
    INCORRECT_NAME_FORMAT: str = (
        "Некорректный формат имени. Пожалуйста, укажите имя и фамилию в "
        "формате 'Имя Фамилия'."
    )
    PHONE_NUMBER_QUESTION: str = "Укажите ваш номер телефона в формате +7XXXXXXXXXX."
    INCORRECT_PHONE_NUMBER: str = "Неверный формат номера."
    POINT_ID_QUESTION: str = "Укажите ID пункта, в котором вы работаете."
    INCORRECT_POINT_ID: str = (
        "Пункт с таким ID не найден. Пожалуйста, проверьте введенный ID и "
        "попробуйте снова."
    )
    INCORRECT_POINT_ID_FORMAT = "ID должен быть числом"
