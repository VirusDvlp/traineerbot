from aiogram import types, Dispatcher
from aiogram.dispatcher.storage import FSMContext
from aiogram.dispatcher.filters import Text


from FSM import MainAdminFSM, MailingFSM
from keyboards import get_choice_change_kb, get_main_kb


async def set_admin_mode(message: types.Message):
    await message.answer('Открыта панель администратора', reply_markup=get_choice_change_kb())
    await MainAdminFSM.admin_state.set()


async def exit_change_mode(message: types.Message, state: FSMContext):
    await MainAdminFSM.admin_state.set()
    await message.answer('👍', reply_markup=get_choice_change_kb())

    
async def close_admin_mode(message: types.Message, state: FSMContext):
    await message.answer('Панель администратора закрыта', reply_markup=get_main_kb(message.from_user.id))
    await state.finish()


def register_main_admin_handlers(dp: Dispatcher) -> None:
    dp.register_message_handler(set_admin_mode, Text('АДМИН-ПАНЕЛЬ💻'))
    dp.register_message_handler(
        exit_change_mode,
        Text(startswith='ОТМЕНИТЬ '),
        state=MailingFSM.all_states
        )
    dp.register_message_handler(close_admin_mode, Text('ВЫЙТИ ИЗ РЕЖИМА АДМИНИСТРТАТОРА🔙'), state=MainAdminFSM.admin_state)