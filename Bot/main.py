from aiogram import executor
from create_bot import dp, db
from handlers import register_all_handlers


async def __on_startup(dp):
    '''registering all hadnlers and print about succesfull running'''

    register_all_handlers(dp)
    print('Бот усешно запущен')


async def __on_shut_down(dp):
    db.close_db()
    print('Бот завершил свою работу')


def main() -> None:
    '''start bot working'''
    executor.start_polling(dp, skip_updates=True, on_startup=__on_startup, on_shutdown=__on_shut_down)