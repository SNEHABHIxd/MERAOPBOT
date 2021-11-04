import requests
from pyrogram import Client as Bot


from config import API_HASH, API_ID, BG_IMAGE, BOT_TOKEN
from handlers import __version__

response = requests.get(BG_IMAGE)
with open("./etc/snehuxabhi.jpg", "wb") as file:
    file.write(response.content)


bot = Bot(
    ":memory:",
    API_ID,
    API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root="SNEHABHI"),
)

print(f"[INFO]: SNEHABHI MUSICS v{__version__} STARTED !")

bot.start()
run()
