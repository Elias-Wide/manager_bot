from aiogram.fsm.state import State, StatesGroup


class RegistrationStates(StatesGroup):

    consent_confirm = State()
    name_question = State()
    phone_number_question = State()
    point_id_question = State()
    finished = State()


class AdminStates(StatesGroup):

    dwnld_points = State()
    updt_points = State()


class ProfileStates(StatesGroup):

    set_schedule = State()
