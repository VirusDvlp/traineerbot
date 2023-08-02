from aiogram.dispatcher.filters.state import StatesGroup, State


class MailingFSM(StatesGroup):
    photo_state = State()
    text_state = State()
    add_button_state = State()
    button_text_state = State()
    button_url_state = State()
