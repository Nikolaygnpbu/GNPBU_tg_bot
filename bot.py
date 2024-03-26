import asyncio
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot, Dispatcher
from config_data.config import Config, load_config
from handlers import other_handlers, user_handlers, registration_user_handlers, add_to_repository_handlers, \
    add_remove_unreg_users_handlers, get_statistics
from process import process_serch_new_users
from aiogram.types import BotCommand
import datetime

# Инициализируем логгер
logger = logging.getLogger(__name__)

# Загружаем конфиг в переменную config
config: Config = load_config()
# Инициализируем бот и диспетчер
bot = Bot(token=config.tg_bot.token,
          parse_mode='HTML')
dp = Dispatcher()


# Функция конфигурирования и запуска бота

async def main():
    # Конфигурируем логирование
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')

    # Выводим в консоль информацию о начале запуска бота
    logger.info('Starting bot')

    main_menu_commands = [
        BotCommand(command='/start',
                   description='Старт'),
        BotCommand(command='/cancel',
                   description='Остановка процесса добавления данных'),
        BotCommand(command='/help',
                   description='Справка по работе бота'),


    ]
    await bot.set_my_commands(main_menu_commands)

    # Регистриуем роутеры в диспетчере
    dp.include_router(user_handlers.router)
    dp.include_router(get_statistics.router)
    dp.include_router(registration_user_handlers.router)
    dp.include_router(add_to_repository_handlers.router)
    dp.include_router(add_remove_unreg_users_handlers.router)
    dp.include_router(other_handlers.router)

    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    scheduler.add_job(process_serch_new_users.serch_new_users, trigger='cron', hour=10, minute=0,
                      start_date=datetime.datetime.now())
    scheduler.add_job(process_serch_new_users.serch_new_users, trigger='cron', hour=14, minute=0,
                      start_date=datetime.datetime.now())
    scheduler.add_job(process_serch_new_users.serch_new_users, trigger='cron', hour=17, minute=0,
                      start_date=datetime.datetime.now())
    scheduler.start()
    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
