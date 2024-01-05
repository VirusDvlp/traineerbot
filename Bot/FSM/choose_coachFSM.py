from aiogram.dispatcher.filters.state import StatesGroup, State


class ChooseCoachFSM(StatesGroup):
    search_state = State()
    choose_state = State()
    mess_state = State()
    