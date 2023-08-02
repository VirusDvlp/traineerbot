from aiogram import types, Dispatcher
from aiogram.dispatcher.storage import FSMContext
from aiogram.dispatcher.filters import Text

from FSM import MailingFSM, MainAdminFSM
from create_bot import db
from keyboards import get_add_bt_kb, get_cancel_kb, get_choice_change_kb


async def make_mailing(message: types.Message):
    await message.answer('Пришлите фотографию к вашей рассылке', reply_markup=get_cancel_kb('РАССЫЛКУ'))
    await MailingFSM.photo_state.set()


async def get_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    await message.answer('Теперь пришлите текст сообщения в вашей рассылке')
    await MailingFSM.text_state.set()


async def get_text(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['text'] = message.text
        data['keyboard'] = types.InlineKeyboardMarkup(1)
        await message.answer_photo(
            data['photo'],
            'СЕЙЧАС ВАШЕ СООБЩЕНИЕ ВЫГЛЯДЕТ ТАК:\n' + message.text,
            reply_markup=data['keyboard']
        )
    await message.answer('''Теперь определите будут ли в вашем сообщении кнопки\n
    Если да, то нажмите "ДОБАВИТЬ КНОПКУ", а если нет, то кнопку ниже
    (Учтите, что после этого собщение разошлется всем пользователям)''',
    reply_markup=get_add_bt_kb())
    await MailingFSM.add_button_state.set()
    

async def add_bt(callback: types.CallbackQuery):
    await callback.message.answer('Пришлите текст вашей кнопки')
    await MailingFSM.button_text_state.set()
    await callback.answer()


async def get_bt_text(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['bt_text'] = message.text
    await message.answer('Теперь пришлите ссылку, на которую будет ввести кнопка')
    await MailingFSM.button_url_state.set()


async def get_bt_url(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['keyboard'].add(types.InlineKeyboardButton(data['bt_text'], message.text))
        await message.answer_photo(
            data['photo'],
            'СЕЙЧАС\tВАШЕ\tСООБЩЕНИЕ\tВЫГЛЯДЕТ\tТАК:\n' + data['text'],
            reply_markup=data['keyboard']
        )
    await MailingFSM.add_button_state.set()
    await message.answer('Кнопка\tуспешно\tдобавлена', reply_markup=get_add_bt_kb())


async def send_mailing(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        keyboard = data['keyboard']
        users = db.get_user_id_list()
        for user in users:
            try:
                await callback.bot.send_photo(
                    user['user_id'],
                    photo=data['photo'],
                    caption=data['text'],
                    reply_markup=keyboard
                )
            except Exception:
                continue
    await callback.message.answer('Рассылка\tуспешно\tсоздана', reply_markup=get_choice_change_kb())
    await MainAdminFSM.admin_state.set()
    await callback.answer()


def register_mailing_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(make_mailing, Text('СОЗДАТЬ РАССЫЛКУ ПОЛЬЗОВАТЕЛЯМ✉️'), state=MainAdminFSM.admin_state)
    dp.register_message_handler(get_photo, content_types=['photo'], state=MailingFSM.photo_state)
    dp.register_message_handler(get_text, state=MailingFSM.text_state)
    dp.register_callback_query_handler(add_bt, Text('add_bt'), state=MailingFSM.add_button_state)
    dp.register_message_handler(get_bt_text, state=MailingFSM.button_text_state)
    dp.register_message_handler(get_bt_url, state=MailingFSM.button_url_state)
    dp.register_callback_query_handler(send_mailing, Text('send'), state=MailingFSM.add_button_state)
