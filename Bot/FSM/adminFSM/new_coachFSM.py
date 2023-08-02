from aiogram.dispatcher.filters.state import StatesGroup, State



class NewCoachFSM(StatesGroup):
    full_name_state = State()
    exp_state = State()
    specializ_state = State()
    photo_state = State()
