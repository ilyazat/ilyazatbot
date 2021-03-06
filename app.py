from aiogram import executor
from utils.set_bot_commands import set_default_commands
from utils.notify_admins import on_startup_notify




async def on_startup(disp):
    await on_startup_notify(disp)
    await set_default_commands(disp)


if __name__ == '__main__':
    from handlers.movie_handler import dp
    executor.start_polling(dp, on_startup=on_startup)
