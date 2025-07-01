from aiogram.fsm.state import State, StatesGroup


class RegistrationStates(StatesGroup):
    """
    States for the user registration process.

    consent_confirm: State where the user confirms consent to data processing.
    name_question: State where the user is asked to enter their name and surname.
    phone_number_question: State where the user is asked to enter their phone number.
    point_id_question: State where the user is asked to enter the office (point) ID.
    finished: State indicating the registration process is complete.
    """

    consent_confirm = State()
    name_question = State()
    phone_number_question = State()
    point_id_question = State()
    finished = State()


class AdminStates(StatesGroup):
    """
    States for admin actions in the admin panel.

    dwnld_points: State for downloading office (point) data.
    updt_points: State for updating office (point) data.
    """

    dwnld_points = State()
    updt_points = State()


class ProfileStates(StatesGroup):
    """
    States for user profile management.

    set_schedule: State for setting or editing the user's work schedule.
    """

    set_schedule = State()


class ReportsStates(StatesGroup):
    """
    States for generating and sending reports.

    choose_office: State for selecting an office (point) for the report.
    send_photo: State for sending a photo as part of the report.
    """

    choose_office = State()
    send_photo = State()
