import os
from dotenv import load_dotenv
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from create_bot import db

load_dotenv()

def get_main_kb(user_id: int) -> ReplyKeyboardMarkup:
    main_kb = ReplyKeyboardMarkup(resize_keyboard=True)
    if user_id in db.get_coach_id_list():
        edit_bt = KeyboardButton('ИЗМЕНИТЬ ПАРАМЕТРЫ ПРОФИЛЯ⚙')
        client_con_br = KeyboardButton('СВЯЗЬ С КЛИЕНТАМИ')
        main_kb.add(edit_bt)
    else:
        make_train_bt = KeyboardButton('ЗАПИСАТЬСЯ НА ТРЕНИРОВКУ📝')
        coach_con_bt = KeyboardButton('СВЯЗЬ С ТРЕНЕРОМ📞')
        main_kb.add(make_train_bt).add(coach_con_bt)
        if user_id == int(os.getenv('ADMIN_ID')):
            admin_bt = KeyboardButton('АДМИН-ПАНЕЛЬ💻')
            main_kb.add(admin_bt)
    return main_kb


def get_choice_user_type_kb() -> ReplyKeyboardMarkup:
    choice_user_type_kb = ReplyKeyboardMarkup(resize_keyboard=True)
    client_bt = KeyboardButton('ВОЙТИ КАК ПОСЕТИТЕЛЬ')
    coach_bt = KeyboardButton('ВОЙТИ КАК ТРЕНЕР')
    return choice_user_type_kb.add(client_bt, coach_bt)
