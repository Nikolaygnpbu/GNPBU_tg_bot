import asyncio
import logging

from aiogram import Bot, Dispatcher

from config_data.config import Config, load_config
from handlers import other_handlers, user_handlers, registration_user_handlers,add_to_repository_handlers
from aiogram.types import BotCommand
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

#
    main_menu_commands = [
        BotCommand(command='/start',
                   description='Старт'),
        BotCommand(command='/cancel',
                   description='Остановка процесса добавления данных'),
        BotCommand(command='/help',
                   description='Справка по работе бота'),
        # BotCommand(command='/contacts',
        #            description='Другие способы связи')

    ]
    await bot.set_my_commands(main_menu_commands)

    # Регистриуем роутеры в диспетчере
    dp.include_router(user_handlers.router)
    dp.include_router(registration_user_handlers.router)
    dp.include_router(add_to_repository_handlers.router)
    dp.include_router(other_handlers.router)

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())