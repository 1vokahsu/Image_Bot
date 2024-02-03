import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import CallbackQuery, Message
from core.config.config import config
from core.handlers import basic
from core.menu.set_meny_button import set_main_menu


async def run_bot():
    # Логирование
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - [%(levelname)s] - %(name)s - "
               "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
    )
    # Добавляем обьекты бота
    bot = Bot(token=config.bot_token.get_secret_value(),
              parse_mode='HTML')
    dp = Dispatcher(bot=bot)
    await bot.delete_webhook(drop_pending_updates=True)
    dp.startup.register(set_main_menu)
    dp.include_router(basic.router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(run_bot())
