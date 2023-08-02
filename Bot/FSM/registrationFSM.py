from aiogram.dispatcher.filters.state import StatesGroup, State


class RegistrationFSM(StatesGroup):
    user_type_state = State()
    name_state = State()
    phone_number_state = State()
    weight_state = State()

    token_state = State()
