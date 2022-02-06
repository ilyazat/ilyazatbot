from aiogram import types

from loader import dp, db


@dp.message_handler(commands=["history"])
async def get_history(message: types.Message):
    res = []
    for date, movie in db.get_history_10(message.from_user.id):
        res.append(f"Date: {date}, Movie: {movie}")
    await message.reply("\n\n".join(res))


@dp.message_handler(commands=["last"])
async def get_last_movie(message: types.Message):
    await message.reply(db.get_last_record(message.from_user.id))
