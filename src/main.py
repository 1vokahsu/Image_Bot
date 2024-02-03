import asyncio
import logging
from aiogram import Bot
from core.config.config import config
from create_dp import dp
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

    await bot.delete_webhook(drop_pending_updates=True)
    dp.startup.register(set_main_menu)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(run_bot())
