'''Handlers for adding user in data base'''

from aiogram import types, Dispatcher
from aiogram.dispatcher.storage import FSMContext
from aiogram.dispatcher.filters import Text

from create_bot import db
from FSM import RegistrationFSM
from utils import check_number
from keyboards import get_main_kb, get_choice_user_type_kb


async def ask_user_type(message: types.Message):
    await RegistrationFSM.user_type_state.set()
    await message.answer('Здравствуйте!\nВам необходимо зарегистрироваться\nКак вы хотите войти?', reply_markup=get_choice_user_type_kb())


async def ask_full_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['user_id'] = message.from_user.id
    await RegistrationFSM.name_state.set()
    await message.answer(
        text='''Пришлите своё имя, фамилия и отчество(если есть)''',
        reply_markup=None
    )


async def ask_phone_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['full_name'] = message.text
    await RegistrationFSM.next()
    await message.answer(
        text='Отлично! Теперь пришлите свой номер телефона в формате 8xxxxxxxx'
    )


async def get_wrong_phone_number(message: types.Message):
    await message.answer('Неверно указан номер телефона попробуйте еще раз')


async def ask_weight(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone_number'] = message.text
    await RegistrationFSM.next()
    await message.answer(
        'Хорошо. Теперь пришлите свой вес с точностью до десятых килограмма(пример: 75.6)'
    )


async def finish_registration(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            data['weight'] = float(message.text)
        except Exception as ex:
            print(ex)
            await message.answer('Что-то пошло не так, попробуйте еще раз и убедитесь, что указали вес верно')
            return None
        db.add_user(
            data['user_id'],
            data['phone_number'],
            data['weight'],
            data['full_name']
        )
        await message.answer(
            '''Вы успешно зарегистрировались в телеграмм-бот нашего Фитнес-клуба
Вы можете прямо здесь записаться тренировку с любым из нашем тренеров
(для этого нажмите на кнопку "ЗАПИСАТЬСЯ НА ТРЕНИРОВКУ").\n
Также вы можете прямо здесь общаться с тренером, на тренировку которого вы записаны
(кнопка "СВЯЗЬ С ТРЕНЕРОМ")\n
Если бот не отвечает долгое время, то перезапустите его командой /start а если и это не помогло,
то напишите нам в тех. поддержку - biznes-fitnes-help@gamil.com''',
            reply_markup=get_main_kb(message.from_user.id)
        )
    await state.finish()


async def ask_token(message: types.Message):
    await RegistrationFSM.token_state.set()
    if not db.check_coach_init(message.from_user.id):
        await message.answer('Пришлите свой токен тренера(его можно попросить у администратора)', reply_markup=None)
    else:
        await message.answer('''Тренер уже зарегистрирован,
 если это реально вы, то обратитесь в тех поддержку biznes-fitnes-help@gamil.com\n
А сейчас перезапустите бота с помощью команды /start''', reply_markup=None)


async def init_coach(message: types.Message, state: FSMContext):
    db.init_coach(message.from_user.id, message.text)
    await state.finish()
    await message.answer('Вы успешно вошли как тренер', reply_markup=get_main_kb(message.from_user.id))


def register_registration_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(ask_full_name, Text('ВОЙТИ КАК ПОСЕТИТЕЛЬ'), state=RegistrationFSM.user_type_state)
    dp.register_message_handler(ask_phone_number, state=RegistrationFSM.name_state)
    dp.register_message_handler(ask_weight, lambda message: check_number(message), state=RegistrationFSM.phone_number_state)
    dp.register_message_handler(get_wrong_phone_number, state=RegistrationFSM.phone_number_state)
    dp.register_message_handler(finish_registration, state=RegistrationFSM.weight_state)
    dp.register_message_handler(ask_token, Text('ВОЙТИ КАК ТРЕНЕР'), state=RegistrationFSM.user_type_state)
    dp.register_message_handler(init_coach, state=RegistrationFSM.token_state)
