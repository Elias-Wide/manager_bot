class Captions:
    no_caption: str = ""

    bot_first_message: str = (
        "Привет! Я бот для менеджеров ВБ. Чтобы начать, мне нужно немного "
        "информации о тебе."
    )
    name_question: str = "Укажите ваше имя и фамилию в формате 'Имя Фамилия'."
    incorrect_name_format: str = (
        "Некорректный формат имени. Пожалуйста, укажите имя и фамилию в формате "
        "'Имя Фамилия'."
    )
    phone_number_question: str = (
        "Укажите ваш номер телефона в формате +7XXXXXXXXXX."
    )
    incorrect_phone_number: str = "Неверный формат номера."
    point_id_question: str = "Укажите ID пункта, в котором вы работаете."
    incorrect_point_id: str = (
        "Пункт с таким ID не найден. Пожалуйста, проверьте введенный ID и "
        "попробуйте снова."
    )
    incorrect_point_id_format: str = "ID должен быть числом"

    def __getattr__(self, name):
        return self.no_caption


captions = Captions()
