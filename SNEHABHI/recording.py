from os import path

import converter
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
    lel = await message.reply_text("π **πΏππΎπ²π΄πππΈπ½πΆ ππΎππ½π³** ...")

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="β¨ Ι’Κα΄α΄α΄", url=f"https://t.me/{GROUP_SUPPORT}"
                ),
                InlineKeyboardButton(
                    text="π» α΄Κα΄Ι΄Ι΄α΄Κ", url=f"https://t.me/{UPDATES_CHANNEL}"
                ),
            ]
        ]
    )

    audio = message.reply_to_message.audio if message.reply_to_message else None
    if not audio:
        return await lel.edit("π­ **πΏπ»π΄π°ππ΄ ππ΄πΏπ»π ππΎ π° ππ΄π»π΄πΆππ°πΌ π°ππ³πΈπΎ π΅πΈπ»π΄ **")
    if round(audio.duration / 60) > DURATION_LIMIT:
        return await lel.edit(
            f"β **πΌπππΈπ² ππΈππ· π³πππ°ππΈπΎπ½ πΌπΎππ΄ ππ·π°π½** `{DURATION_LIMIT}` **πΌπΈπ½πππ΄π π²π°π½'π πΏπ»π°π !**"
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
            caption=f"π‘ **Track added to queue Β»** `{position}`\n\nπ· **Name:** {title[:50]}\nβ± **Duration:** `{duration}`\nπ§ **Request by:** {costumer}",
            reply_markup=keyboard,
        )
    else:
        callsmusic.pytgcalls.join_group_call(message.chat.id, file_path)
        await message.reply_photo(
            photo=f"{AUD_IMG}",
            caption=f"π· **Name:** {title[:50]}\nβ± **Duration:** `{duration}`\nπ‘ **Status:** `Playing`\n"
            + f"π§ **Request by:** {costumer}",
            reply_markup=keyboard,
        )

    return await lel.delete()
