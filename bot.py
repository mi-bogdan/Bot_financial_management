import logging

from aiogram import Bot, Dispatcher

from core.handlers.main_handlers import router
from core.handlers.registration import router_register
from core.settings import config
from core.utils.commands import set_commands

# from core.db.queries import DataBase


async def start_bot(bot: Bot) -> None:
    await set_commands(bot)
    await bot.send_message(config.bots.admin_id, text="<b>Бот запущен!</b>")


async def stop_bot(bot: Bot) -> None:
    await bot.send_message(config.bots.admin_id, text="<b>Бот остановлен!</b>")


# Настройка логирования
logging.basicConfig(level=logging.INFO)


async def main() -> None:
    # Инициализация бота и диспетчера
    bot = Bot(token=config.bots.bot_token, parse_mode="HTML")
    dp = Dispatcher()
    await set_commands(bot)
    # Регистрируем роутеры хендлеров
    dp.include_router(router).include_router(router_register)
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    # Настройка диспетчера и запуск обработчиков
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    # Запуск основной асинхронной функции
    import asyncio

    asyncio.run(main())
