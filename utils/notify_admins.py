import logging

from aiogram import Dispatcher

from data.config import admin


async def on_startup_notify(dp: Dispatcher):
    try:
        await dp.bot.send_message(admin, "Бот Запущен и готов к работе, админ")

    except Exception as err:
        print(err)
        logging.exception(err)
