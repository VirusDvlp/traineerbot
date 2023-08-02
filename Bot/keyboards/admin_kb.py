from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton



def get_choice_change_kb() -> ReplyKeyboardMarkup:
    choice_change_kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    mailing_bt = KeyboardButton('СОЗДАТЬ РАССЫЛКУ ПОЛЬЗОВАТЕЛЯМ✉️')
    new_coach_bt = KeyboardButton('ДОБАВИТЬ ТРЕНЕРА➕')
    exit_bt = KeyboardButton('ВЫЙТИ ИЗ РЕЖИМА АДМИНИСТРТАТОРА🔙')
    return choice_change_kb.add(mailing_bt, new_coach_bt, exit_bt)



def get_cancel_kb(input_data: str) -> ReplyKeyboardMarkup:
    cancel_bt = KeyboardButton(f'ОТМЕНИТЬ {input_data}✖️')
    mailing_kb = ReplyKeyboardMarkup().add(cancel_bt)
    return mailing_kb


def get_add_bt_kb() -> InlineKeyboardMarkup:
    add_bt = InlineKeyboardButton('ДОБАВИТЬ КНОПКУ', callback_data='add_bt')
    send_bt = InlineKeyboardButton('ОТПРАВИТЬ РАССЫЛКУ', callback_data='send')
    return InlineKeyboardMarkup(1).add(add_bt, send_bt)
