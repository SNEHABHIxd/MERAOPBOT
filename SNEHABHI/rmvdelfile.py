import os

from pyrogram import Client, filters
from pyrogram.types import Message

from config import BOT_USERNAME
from helpers.decorators import errors, sudo_users_only
from helpers.filters import command

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
        await message.reply_text("✅ **𝚁𝙴𝙼𝙾𝚅𝙴𝙳 𝙰𝙻𝙻 𝙳𝙾𝚆𝙽𝙻𝙾𝙰𝙳𝙴𝙳 𝙵𝙸𝙻𝙴𝚂**")
    else:
        await message.reply_text("❌ **𝙽𝙾 𝙵𝙸𝙻𝙴𝚂 𝙸𝚂 𝙳𝙾𝚆𝙽𝙻𝙾𝙰𝙳𝙴𝙳**")
