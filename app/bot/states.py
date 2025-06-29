from aiogram.fsm.state import State, StatesGroup


class RegistrationStates(StatesGroup):

    consent_confirm = State()
    name_question = State()
    phone_number_question = State()
    point_id_question = State()
    finished = State()
