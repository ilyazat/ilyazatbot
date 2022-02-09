from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand("start", "Start the bot"),
        types.BotCommand("help", "Call helper"),
        types.BotCommand("history", "Show your query history")
    ])
