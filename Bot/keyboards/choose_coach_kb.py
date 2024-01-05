from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


def get_main_choose_coach_kb() -> ReplyKeyboardMarkup:
    main_choose_coach_kb = ReplyKeyboardMarkup(resize_keyboard=True)
    all_coaches_bt = KeyboardButton('ВСЕ ТРЕНЕРЫ💪')
    return main_choose_coach_kb.add(all_coaches_bt)


def get_choose_coach_kb(id: int) -> InlineKeyboardMarkup:
    choose_coach_kb = InlineKeyboardMarkup(1)
    choose_bt = InlineKeyboardButton('ЗАПИСАТЬСЯ', callback_data=f'coach_{id}')
    return choose_coach_kb.add(choose_bt)
