import os

from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = str(os.getenv("BOT_TOKEN"))
admin = int(os.getenv("admin"))
imdb_token = str(os.getenv("imdb_token"))
