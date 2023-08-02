from aiogram.dispatcher.filters.state import StatesGroup, State


class MainAdminFSM(StatesGroup):
    admin_state = State()