from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import ParseMode

from FSM import NewCoachFSM, MainAdminFSM
from keyboards import get_cancel_kb, get_choice_change_kb
from create_bot import db
from utils import generate_id


async def ask_coach_name(message: types.Message):
    await NewCoachFSM.full_name_state.set()
    await message.answer('Напишите ФИО тренера', reply_markup=get_cancel_kb('ДОБАВЛЕНИЕ ТРЕНЕРА'))    


async def ask_coach_experience(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await NewCoachFSM.next()
    await message.answer('Напишите стаж тренера(только цифра)')


async def ask_coach_spec(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            data['exp'] = int(message.text)
        except Exception as ex:
            print(ex)
            await message.answer('Указывайте только число. Попробуйте еще раз')
    await NewCoachFSM.next()
    await message.answer(
        '''Теперь через запятую(без пробелов) укажите
специализацию тренера, по ней клиенты смогут быстро находить себе нужного наставника.
Например: похудение,борьба,кросс-фит,плавание\nЧем больше тем лучше'''
    )


async def ask_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['spec'] = message.text
    await NewCoachFSM.next()
    await message.answer('Пришлите фотографию тренера, которая будет отображаться пользователям')


async def finish_coach(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
        token = generate_id()
        db.add_coach(data['name'], data['exp'], data['spec'], data['photo'], token)
        await message.answer(
            f'''Тренер успешно добавлен. Чтобы войти, он должен при
регистрации нажать \'войти как тренер\' и далее указать его
 уникальный токен - `{token}`\nКроме тренера никому не сообщайте токен, а то могу возникнуть неприятности''',
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=get_choice_change_kb()
        )
    await MainAdminFSM.admin_state.set()


def register_new_coach_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(ask_coach_name, Text('ДОБАВИТЬ ТРЕНЕРА➕'), state=MainAdminFSM.admin_state)
    dp.register_message_handler(ask_coach_experience, state=NewCoachFSM.full_name_state)
    dp.register_message_handler(ask_coach_spec, state=NewCoachFSM.exp_state)
    dp.register_message_handler(ask_photo, state=NewCoachFSM.specializ_state)
    dp.register_message_handler(finish_coach, state=NewCoachFSM.photo_state, content_types=['photo'])
