import os

from pyrogram import Client, filters
from pyrogram.types import Message

from config import BOT_USERNAME
from SNEHABHI.SNEHUABHI.decorators import errors, sudo_users_only
from SNEHABHI.SNEHUABHI.filters import command

downloads = os.path.realpath("downloads")
raw = os.path.realpath("raw_files")


@Client.on_message(command(["rmd", "clean", f"rmd@{BOT_USERNAME}", f"clean@{BOT_USERNAME}"]) & ~filters.edited)
@errors
@sudo_users_only
async def clear_downloads(_, message: Message):
    ls_dir = os.listdir(downloads)
    if ls_dir:
        for file in os.listdir(downloads):
            os.remove(os.path.join(downloads, file))
        await message.reply_text("β **ππ΄πΌπΎππ΄π³ π°π»π» π³πΎππ½π»πΎπ°π³π΄π³ π΅πΈπ»π΄π**")
    else:
        await message.reply_text("β **π½πΎ π΅πΈπ»π΄π πΈπ π³πΎππ½π»πΎπ°π³π΄π³**")
