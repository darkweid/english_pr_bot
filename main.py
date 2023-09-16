import asyncio, logging, sqlite_db

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage, Redis
from config_data.config import Config, load_config
from handlers.user_handlers import user_router
from handlers.admin_handlers import admin_router
from keyboards.set_menu import set_main_menu

# Инициализируем логгер
logger = logging.getLogger(__name__)

config: Config = load_config()
BOT_TOKEN: str = config.tg_bot.token
ADMINS: list = config.tg_bot.admin_ids


async def send_message_to_admin(bot: Bot, text=''):
    for elem in ADMINS:
        await bot.send_message(elem, text=text)


async def main():
    try:

        # Запускаем бота и пропускаем все накопленные входящие
        # Конфигурируем логирование
        logging.basicConfig(#filename='bot.log',
                            level=logging.INFO,
                            format='#%(levelname)-8s '
                                   '[%(asctime)s] - %(name)s - %(message)s')

        # Выводим в консоль информацию о начале запуска бота
        logger.info('Starting bot')
        # Инициализируем Redis
        redis: Redis = Redis(host='localhost')
        storage: RedisStorage = RedisStorage(redis=redis)
        superadmin = config.tg_bot.admin_ids[0]
        # запускаем БД sqlite3
        await sqlite_db.sql_start()
        bot: Bot = Bot(token=BOT_TOKEN, parse_mode='HTML')
        dp: Dispatcher = Dispatcher(storage=storage)
        # Регистрируем роутеры в диспетчере
        dp.include_router(admin_router)
        dp.include_router(user_router)
        # Настраиваем главное меню
        await set_main_menu(bot)
        await bot.delete_webhook(drop_pending_updates=True)
        await send_message_to_admin(bot, text='Бот запущен!')
        await dp.start_polling(bot, )
    except Exception as e:
        logger.exception("Ошибка: %s", str(e))

    finally:
        logger.info("Бот был остановлен.")
        await send_message_to_admin(bot, text='Бот остановлен!')


# if __name__ == "__main__":
#    asyncio.run(main())
#    keep_alive()
#    dp.startup.register(set_main_menu)

if __name__ == "__main__":
    asyncio.run(main())
