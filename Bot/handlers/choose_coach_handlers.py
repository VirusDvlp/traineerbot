from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text

from create_bot import db
from FSM import ChooseCoachFSM
from keyboards import get_main_choose_coach_kb
from utils import get_coach_descr


async def start_coach_searhing(message: types.Message):
    await ChooseCoachFSM.search_state.set()
    await message.answer(
        '''Через запятую(без пробелов) укажите
специализацию тренера, необходимую вам
Например: похудение,борьба,набор массы,плавание\nЧем больше тем лучше.
Если же вы хотите полный список тренеров, то нажмите соответсвующую кнопку внизу.''',
        reply_markup=get_main_choose_coach_kb()
    )


async def full_list_of_coaches(message: types.Message):
    [
        await message.answer_photo(
            coach['photo'],
            get_coach_descr(coach)
        )
        for coach in db.get_coaches(True)
    ]


async def recomended_coaches(message: types.Message):
    coaches = db.get_coaches(False, message.text)
    if coaches:
        [
            await message.answer_photo(
                coach['photo'],
                get_coach_descr(coach)
            )
            for coach in coaches
        ]
    else:
        await message.answer('''Не удалось ничего найти по вашему запросу,
убедитесь, что указано всё правильно или добавьте ещё специализаций'''
        )


def register_choose_coach_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(start_coach_searhing, Text('ЗАПИСАТЬСЯ НА ТРЕНИРОВКУ📝'))
    dp.register_message_handler(
        full_list_of_coaches,
        Text('ВСЕ ТРЕНЕРЫ💪'),
        state=ChooseCoachFSM.search_state
    )
    dp.register_message_handler(
        recomended_coaches,
        content_types=['text'],
        state=ChooseCoachFSM.search_state
    )