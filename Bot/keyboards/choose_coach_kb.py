from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_main_choose_coach_kb() -> ReplyKeyboardMarkup:
    main_choose_coach_kb = ReplyKeyboardMarkup(resize_keyboard=True)
    all_coaches_bt = KeyboardButton('ВСЕ ТРЕНЕРЫ💪')
    return main_choose_coach_kb.add(all_coaches_bt)
