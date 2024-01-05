from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.storage import FSMContext

from create_bot import db
from FSM import ChooseCoachFSM
from keyboards import get_main_choose_coach_kb, get_choose_coach_kb
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
            get_coach_descr(coach),
            reply_markup=get_choose_coach_kb(coach['user_id'])
        )
        for coach in db.get_coaches(True)
    ]


async def recomended_coaches(message: types.Message):
    coaches = db.get_coaches(False, message.text)
    if coaches:
        [
            await message.answer_photo(
                coach['photo'],
                get_coach_descr(coach),
                reply_markup=get_choose_coach_kb(coach['user_id'])
            )
            for coach in coaches
        ]
    else:
        await message.answer('''Не удалось ничего найти по вашему запросу,
убедитесь, что указано всё правильно или добавьте ещё специализаций'''
        )


async def ask_message_to_coach(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['coach'] = callback.data.split('_')[1]
    await callback.message.answer(
        '''Теперь напишите сообщение, которое хотите оставить в заявке к тренеру.
Осталвяя заявку, вы даёте согласие на то, что вашие данные будут переданы тренеры(ФИО, вес и возраст)
'''
)


async def create_training(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        user = db.check_user_exists(message.from_user.id)
        await message.bot.send_message(
            data['coach'],
            f'''
Вам новая заявка от {user['full_name']}\n\n
Текст заявки:\n{message.text}\n\n
Возраст: {user['age']}\n
Вес: {user['weight']}\n\n
Для общения с клиентом нажмите на кнопку "СВЯЗЬ С КЛИЕНТАМИ" и выберите данного человека.
'''
        )
        await state.finish()
        await message.answer(
            '''Ваша заявка успешно передана тренеру, как только тренер прочтёт вашу заявку и ответит
на неё, мы сообщим вам. Также вы можете написать ещё сообщений тренеру во вкладке "СВЯЗЬ С ТРЕНЕРОМ"
'''
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