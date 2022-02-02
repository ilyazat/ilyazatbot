import math

from aiogram import types

from loader import dp, bot, db
from data.config import imdb_token
from apis.imdb_api import IMDbSession


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    greet_photo = "https://sun9-24.userapi.com/impg/cxB56z6cKXnOuhHq4kS_vomHW1OyvPKfrhoFfw/HhdCGnmWIV0.jpg" \
                  "?size=640x480&quality=96&sign=5f84ecb9a62e7fc3e0037de637a20379&type=album"
    await bot.send_photo(
        message.from_user.id,
        photo=greet_photo
    )
    await message.reply(f"Hey, {message.from_user.full_name}! I can process movie title!")


@dp.message_handler(commands=["help"])
async def helper(message: types.Message):
    await message.reply("Hi! \nThis helper to help you with !")


@dp.message_handler(commands=["history"])
async def get_history(message: types.Message):
    res = []
    for date, movie in db.get_history_10(message.from_user.id):
        res.append(f"Date: {date}, Movie: {movie}")
    await message.reply("\n\n".join(res))


@dp.message_handler(commands=["my_id"])
async def get_user_id(message: types.Message):
    await bot.send_message(message.from_user.id, message.from_user.id)


@dp.message_handler(commands=["last"])
async def get_last_movie(message: types.Message):
    await message.reply(db.get_last_record(message.from_user.id))


@dp.message_handler()
async def movie_handler(message: types.Message):
    imdb_result = await IMDbSession(imdb_token, language="ru").search_by_expression_imdb(message.text)

    if imdb_result:
        print(len(imdb_result.image))
        reply = f"<b>Title</b>:\n{imdb_result.fullTitle}\n\n" \
                f"<b>Type</b>:\n{imdb_result.type}\n\n" \
                f"<b>Plot</b>:\n{imdb_result.plot}\n\n" \
                f"<b>IMDb Rating</b>:\n{float(imdb_result.imDbRating)} {math.ceil(float(imdb_result.imDbRating)) * '⭐'}"
        db.add_to_history(user_id=message.from_user.id,
                          query=message.text,
                          status="ok",
                          movie=imdb_result.fullTitle)
        try:
            await bot.send_photo(message.from_user.id,
                                 imdb_result.image,
                                 caption=reply)
            return
        except:
            await bot.send_document(message.from_user.id, imdb_result.image)
            await bot.send_message(message.from_user.id, reply)
            return
    else:
        await message.reply("Sorry, the movie couldn't be found")
        return
