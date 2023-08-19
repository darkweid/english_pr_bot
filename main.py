import asyncio, logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage, Redis
from config_data.config import Config, load_config
from handlers.user_handlers import user_router
from handlers.admin_handlers import admin_router
from keyboards.set_menu import set_main_menu
import sqlite_db

# Инициализируем логгер
logger = logging.getLogger(__name__)


async def main():
    # Запускаем бота и пропускаем все накопленные входящие
    # Конфигурируем логирование
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')

    # Выводим в консоль информацию о начале запуска бота
    logger.info('Starting bot')
    config: Config = load_config()
    BOT_TOKEN: str = config.tg_bot.token
    ADMINS: list = config.tg_bot.admin_ids
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
    await dp.start_polling(bot, )


# if __name__ == "__main__":
#    asyncio.run(main())
#    keep_alive()
#    dp.startup.register(set_main_menu)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped!")
