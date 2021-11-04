from os import path

import SNEHABHI.converter
from SNEHABHI.callsmusic import callsmusic, queues
from config import (
    AUD_IMG,
    BOT_USERNAME,
    DURATION_LIMIT,
    GROUP_SUPPORT,
    QUE_IMG,
    UPDATES_CHANNEL,
)
from SNEHABHI.abhishek import convert_seconds
from SNEHABHI.SNEHUABHI.filters import command, other_filters
from SNEHABHI.SNEHUABHI.gets import get_file_name
from pyrogram import Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message


@Client.on_message(command(["play", f"play@{BOT_USERNAME}"]) & other_filters)
async def play(_, message: Message):
    costumer = message.from_user.mention
    lel = await message.reply_text("🔁 **𝙿𝚁𝙾𝙲𝙴𝚂𝚂𝙸𝙽𝙶 𝚂𝙾𝚄𝙽𝙳** ...")

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="✨ ɢʀᴏᴜᴘ", url=f"https://t.me/{GROUP_SUPPORT}"
                ),
                InlineKeyboardButton(
                    text="🌻 ᴄʜᴀɴɴᴇʟ", url=f"https://t.me/{UPDATES_CHANNEL}"
                ),
            ]
        ]
    )

    audio = message.reply_to_message.audio if message.reply_to_message else None
    if not audio:
        return await lel.edit("💭 **𝙿𝙻𝙴𝙰𝚂𝙴 𝚁𝙴𝙿𝙻𝚈 𝚃𝙾 𝙰 𝚃𝙴𝙻𝙴𝙶𝚁𝙰𝙼 𝙰𝚄𝙳𝙸𝙾 𝙵𝙸𝙻𝙴 **")
    if round(audio.duration / 60) > DURATION_LIMIT:
        return await lel.edit(
            f"❌ **𝙼𝚄𝚂𝙸𝙲 𝚆𝙸𝚃𝙷 𝙳𝚄𝚁𝙰𝚃𝙸𝙾𝙽 𝙼𝙾𝚁𝙴 𝚃𝙷𝙰𝙽** `{DURATION_LIMIT}` **𝙼𝙸𝙽𝚄𝚃𝙴𝚂 𝙲𝙰𝙽'𝚃 𝙿𝙻𝙰𝚈 !**"
        )

    # tede_ganteng = True
    title = audio.title
    file_name = get_file_name(audio)
    duration = convert_seconds(audio.duration)
    file_path = await converter.convert(
        (await message.reply_to_message.download(file_name))
        if not path.isfile(path.join("downloads", file_name))
        else file_name
    )
    # ambil aja bg
    if message.chat.id in callsmusic.pytgcalls.active_calls:
        position = await queues.put(message.chat.id, file=file_path)
        await message.reply_photo(
            photo=f"{QUE_IMG}",
            caption=f"💡 **Track added to queue »** `{position}`\n\n🏷 **Name:** {title[:50]}\n⏱ **Duration:** `{duration}`\n🎧 **Request by:** {costumer}",
            reply_markup=keyboard,
        )
    else:
        callsmusic.pytgcalls.join_group_call(message.chat.id, file_path)
        await message.reply_photo(
            photo=f"{AUD_IMG}",
            caption=f"🏷 **Name:** {title[:50]}\n⏱ **Duration:** `{duration}`\n💡 **Status:** `Playing`\n"
            + f"🎧 **Request by:** {costumer}",
            reply_markup=keyboard,
        )

    return await lel.delete()
