from aiogram import types

from loader import dp, bot


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
