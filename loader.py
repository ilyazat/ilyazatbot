from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher

from data import config
from apis.db_api import DataBaseHandler, Postgres

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
admin = config.admin
dp = Dispatcher(bot)
db = Postgres("tg", "123")
imdb_token = config.imdb_token

