import math

from aiogram import types, utils
from datetime import datetime

from loader import dp, bot, db
from data.config import imdb_token
from apis.imdb_api import IMDbSession

@dp.message_handler()
async def movie_handler(message: types.Message):
    # if message.text in db.get_ok_queries(user_query=message.text):
    #     bot.send
    #     return
    start = datetime.now()
    imdb_result = await IMDbSession(imdb_token, language="ru").search_by_expression_imdb(message.text)
    if imdb_result:
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
        except utils.exceptions.WrongFileIdentifier:
            await bot.send_message(message.from_user.id, reply)
            return
        except utils.exceptions.BadRequest:
            await bot.send_document(message.from_user.id, imdb_result.image)
            await bot.send_message(message.from_user.id, reply)
            return
        finally:
            print(datetime.now() - start)
    else:
        await message.reply("Sorry, the movie couldn't be found")
        return
