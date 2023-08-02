from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import CommandStart, CommandHelp
from aiogram.dispatcher.storage import FSMContext

from .registration_handlers import ask_user_type
from create_bot import db
from keyboards import get_main_kb


async def start_command(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    await state.finish()
    if db.check_user_exists(user_id) or db.check_coach_init(user_id):
        await help_command(message)
    else:
        await ask_user_type(message)


async def help_command(message: types.Message):
    await message.answer(
        text='''Добро пожаловать в телеграмм-бот нашего Фитнес-клуба
Вы можете прямо здесь записаться тренировку с любым из нашем тренеров
(для этого нажмите на кнопку "ЗАПИСАТЬСЯ НА ТРЕНИРОВКУ").\n
Также вы можете прямо здесь общаться с тренером, на тренировку которого вы записаны
(кнопка "СВЯЗЬ С ТРЕНЕРОМ")\n
Если бот не отвечает долгое время, то перезапустите его командой /start а если и это не помогло,
то напишите нам в тех. поддержку - biznes-fitnes-help@gamil.com''',
        reply_markup=get_main_kb(message.from_user.id)
    )


def register_start_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(start_command, CommandStart(), state='*')
    dp.register_message_handler(help_command, CommandHelp())