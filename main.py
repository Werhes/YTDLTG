import asyncio

# Вручную создаем и устанавливаем цикл событий для Pyrogram
try:
    asyncio.get_event_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

# А уже дальше идут ваши обычные импорты
from pyrogram.raw import functions, types
# ... остальной ваш код ...

from pyrogram.raw import functions, types
from pyrogram import Client, idle
from config import Config

bot = Client(
    "bot",
    bot_token=Config.BOT_TOKEN,
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    workers=50,
    plugins=dict(root="plugins")
)
bot.start()
print("Bot Started ⚡")
idle()
bot.stop()
