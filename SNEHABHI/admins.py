from asyncio import QueueEmpty

from SNEHABHI.callsmusic import callsmusic
from SNEHABHI.callsmusic.queues import queues
from config import BOT_USERNAME, que
from SNEHABHI.cache.admins import admins
from SNEHABHI.abhishek import cb_admin_check
from SNEHABHI.SNEHUABHI.dbtools import delcmd_is_on, delcmd_off, delcmd_on, handle_user_status
from SNEHABHI.SNEHUABHI.decorators import authorized_users_only, errors
from SNEHABHI.SNEHUABHI.filters import command, other_filters
from pyrogram import Client, filters
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)


@Client.on_message()
async def _(bot: Client, cmd: Message):
    await handle_user_status(bot, cmd)


# Back Button
BACK_BUTTON = InlineKeyboardMarkup(
    [[InlineKeyboardButton("π Go Back", callback_data="cbback")]]
)

# @Client.on_message(filters.text & ~filters.private)
# async def delcmd(_, message: Message):
#    if await delcmd_is_on(message.chat.id) and message.text.startswith("/") or message.text.startswith("!") or message.text.startswith("."):
#        await message.delete()
#    await message.continue_propagation()

# remove the ( # ) if you want the auto del cmd feature is on


@Client.on_message(command(["reload", f"reload@{BOT_USERNAME}"]) & other_filters)
async def update_admin(client, message):
    global admins
    new_admins = []
    new_ads = await client.get_chat_members(message.chat.id, filter="administrators")
    for u in new_ads:
        new_admins.append(u.user.id)
    admins[message.chat.id] = new_admins
    await message.reply_text(
        "β Bot **ππ΄π»πΎπ°π³π΄π³ π²πΎπππ΄π²ππ»π ππ½π΄π·π°π±π·πΈ π±πΎππ !**\nβ **π°π³πΌπΈπ»πΈππ** π·π°π π±π΄π΄π½ **ππΏπ³π°ππ΄π³ π±π @SNEHABHI_UPDATES !**"
    )


# Control Menu Of Player
@Client.on_message(command(["control", f"control@{BOT_USERNAME}"]) & other_filters)
@errors
@authorized_users_only
async def controlset(_, message: Message):
    await message.reply_text(
        "π‘ **π·π΄ππ΄ πΈπ ππ·π΄ πΌπ΄π½π π²πΎπ½πππΎπ» πΎπ΅ π±πΎπ :**",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("βΈ pause", callback_data="cbpause"),
                    InlineKeyboardButton("βΆοΈ resume", callback_data="cbresume"),
                ],
                [
                    InlineKeyboardButton("β© skip", callback_data="cbskip"),
                    InlineKeyboardButton("βΉ stop", callback_data="cbend"),
                ],
                [InlineKeyboardButton("β anti cmd", callback_data="cbdelcmds")],
                [InlineKeyboardButton("π Close", callback_data="close")],
            ]
        ),
    )


@Client.on_message(command(["pause", f"pause@{BOT_USERNAME}"]) & other_filters)
@errors
@authorized_users_only
async def pause(_, message: Message):
    chat_id = get_chat_id(message.chat)
    if (chat_id not in callsmusic.pytgcalls.active_calls) or (
        callsmusic.pytgcalls.active_calls[chat_id] == "paused"
    ):
        await message.reply_text("β **π½πΎ πΌπππΈπ² πΈπ π²ππππ΄π½ππ»π πΏπ»π°ππΈπ½πΆ ππΏπ»πΎπ°π³π΄π³ π±π @SNEHABHI_UPDATES**")
    else:
        callsmusic.pytgcalls.pause_stream(chat_id)
        await message.reply_text(
            "βΈ **Track paused.**\n\nβ’ **ππΎ ππ΄πππΌπ΄ ππ·π΄ ππΎπ½πΆ , πππ΄ ππ·π΄**\nΒ» `/resume` π²πΎπΌπΌπ°π½π³ ππΏπ»πΎπ°π³π΄π³ π±π @SNEHABHI_UPDATES."
        )


@Client.on_message(command(["resume", f"resume@{BOT_USERNAME}"]) & other_filters)
@errors
@authorized_users_only
async def resume(_, message: Message):
    chat_id = get_chat_id(message.chat)
    if (chat_id not in callsmusic.pytgcalls.active_calls) or (
        callsmusic.pytgcalls.active_calls[chat_id] == "playing"
    ):
        await message.reply_text("β **π½πΎ πΌπππΈπ² πΈπ πΏπ°πππ΄π³ ππΏπ»πΎπ°π³π΄π³ π±π @SNEHABHI_UPDATES**")
    else:
        callsmusic.pytgcalls.resume_stream(chat_id)
        await message.reply_text(
            "βΆοΈ **Track resumed.**\n\nβ’ **ππΎ πΏπ°πππ΄ ππ·π΄ ππΎπ½πΆ , πππ΄ ππ·π΄**\nΒ» `/pause` π²πΎπΌπΌπ°π½π³ ππΏπ»πΎπ°π³π΄π³ π±π @SNEHABHI_UPDATES."
        )


@Client.on_message(command(["end", f"end@{BOT_USERNAME}"]) & other_filters)
@errors
@authorized_users_only
async def stop(_, message: Message):
    chat_id = get_chat_id(message.chat)
    if chat_id not in callsmusic.pytgcalls.active_calls:
        await message.reply_text("β **π½πΎ πΌπππΈπ² πΈπ π²ππππ΄π½ππ»π πΏπ»π°ππΈπ½πΆ ππΏπ»πΎπ°π³π΄π³ π±π @SNEHABHI_UPDATES**")
    else:
        try:
            queues.clear(chat_id)
        except QueueEmpty:
            pass

        callsmusic.pytgcalls.leave_group_call(chat_id)
        await message.reply_text("β **πΌπππΈπ² ππΎπ½πΆ π·π°π π΄π½π³π΄π³ ππΏπ»πΎπ°π³π΄π³ π±π @SNEHABHI_UPDATES**")


@Client.on_message(command(["skip", f"skip@{BOT_USERNAME}"]) & other_filters)
@errors
@authorized_users_only
async def skip(_, message: Message):
    global que
    chat_id = get_chat_id(message.chat)
    if chat_id not in callsmusic.pytgcalls.active_calls:
        await message.reply_text("β **π½πΎ πΌπππΈπ² πΈπ π²ππππ΄π½ππ»π πΏπ»π°ππΈπ½πΆ ππΏπ»πΎπ°π³π΄π³ π±π @SNEHABHI_UPDATES**")
    else:
        queues.task_done(chat_id)

        if queues.is_empty(chat_id):
            callsmusic.pytgcalls.leave_group_call(chat_id)
        else:
            callsmusic.pytgcalls.change_stream(chat_id, queues.get(chat_id)["file"])

    qeue = que.get(chat_id)
    if qeue:
        qeue.pop(0)
    if not qeue:
        return
    await message.reply_text("β­ **ππΎπ'ππ΄ ππΊπΈπΏπΏπ΄π³ ππΎ ππ·π΄ π½π΄ππ ππΎπ½πΆ π±π @SNEHABHI_UPDATES.**")


@Client.on_message(command(["auth", f"auth@{BOT_USERNAME}"]) & other_filters)
@authorized_users_only
async def authenticate(client, message):
    global admins
    if not message.reply_to_message:
        return await message.reply("π‘ ππ΄πΏπ»π ππΎ πΌππΆ ππΎ π°πππ·πΎππΈππ΄ πππ΄π !")
    if message.reply_to_message.from_user.id not in admins[message.chat.id]:
        new_admins = admins[message.chat.id]
        new_admins.append(message.reply_to_message.from_user.id)
        admins[message.chat.id] = new_admins
        await message.reply(
            "π’ user authorized.\n\nπ΅ππΎπΌ π½πΎπ ππ·π°π'π πππ΄π π²π°π½ πππ΄ ππ·π΄ π°π³πΌπΈπ½ π²πΎπΌπΌπ°π½π³ ππΏπ»πΎπ°π³π΄π³ π±π @SNEHABHI_UPDATES."
        )
    else:
        await message.reply("β πππ΄R π°π»ππ΄π°π³π π°πππ·πΎππΈππ΄π³! ππΏπ»πΎπ°π³π΄π³ π±π @SNEHABHI_UPDATES")


@Client.on_message(command(["deauth", f"deauth@{BOT_USERNAME}"]) & other_filters)
@authorized_users_only
async def deautenticate(client, message):
    global admins
    if not message.reply_to_message:
        return await message.reply("π‘ ππ΄πΏπ»π ππΎ πΌππΆ ππΎ π³π΄π°πππ·πΎππΈππ΄ πππ΄π !")
    if message.reply_to_message.from_user.id in admins[message.chat.id]:
        new_admins = admins[message.chat.id]
        new_admins.remove(message.reply_to_message.from_user.id)
        admins[message.chat.id] = new_admins
        await message.reply(
            "π΄ πππ΄π π³π΄π°πππ·πΎππΈππ΄π³.\n\nπ΅ππΎπΌ π½πΎπ ππ·π°π'π πππ΄π π²π°π½'π πππ΄ ππ·π΄ π°π³πΌπΈπ½ π²πΎπΌπΌπ°π½π³ ππΏπ»πΎπ°π³π΄π³ π±π @SNEHABHI_UPDATES."
        )
    else:
        await message.reply("β πππ΄R π°π»ππ΄π°π³π π³π΄π°πππ·πΎππΈππ΄π³! ππΏπ»πΎπ°π³π΄π³ π±π @SNEHABHI_UPDATES")


# this is a anti cmd feature
@Client.on_message(command(["delcmd", f"delcmd@{BOT_USERNAME}"]) & other_filters)
@authorized_users_only
async def delcmdc(_, message: Message):
    if len(message.command) != 2:
        return await message.reply_text(
            "ππ΄π°π³ ππ·π΄ /help πΌππΆ ππΎ πΊπ½πΎπ π·πΎπ ππΎ πππ΄ ππ·πΈπ π²πΎπΌπΌπ°π½π³ ππΏπ»πΎπ°π³π΄π³ π±π @SNEHABHI_UPDATES"
        )
    status = message.text.split(None, 1)[1].strip()
    status = status.lower()
    chat_id = message.chat.id
    if status == "on":
        if await delcmd_is_on(message.chat.id):
            return await message.reply_text("β π°π»ππ΄π°π³π π°π²ππΈππ°ππ΄π³ ππΏπ»πΎπ°π³π΄π³ π±π @SNEHABHI_UPDATES")
        await delcmd_on(chat_id)
        await message.reply_text("π’ π°π²ππΈππ°ππ΄D πππ²π²π΄πππ΅ππ»π»π  π±π @SNEHABHI_UPDATES")
    elif status == "off":
        await delcmd_off(chat_id)
        await message.reply_text("π΄ π³πΈππ°π±π»π΄π³ πππ²π²π΄πππ΅ππ»π»π  π±π @SNEHABHI_UPDATES")
    else:
        await message.reply_text(
            "ππ΄π°π³ ππ·π΄ /help πΌππΆ ππΎ πΊπ½πΎπ π·πΎπ ππΎ πππ΄ ππ·πΈπ π²πΎπΌπΌπ°π½π³ ππΏπ»πΎπ°π³π΄π³ π±π @SNEHABHI_UPDATES"
        )


# music player callbacks (control by buttons feature)


@Client.on_callback_query(filters.regex("cbpause"))
@cb_admin_check
async def cbpause(_, query: CallbackQuery):
    get_chat_id(query.message.chat)
    if (query.message.chat.id not in callsmusic.pytgcalls.active_calls) or (
        callsmusic.pytgcalls.active_calls[query.message.chat.id] == "paused"
    ):
        await query.edit_message_text(
            "β **π½πΎ ππΎπ½πΆ πΈπ π²ππππ΄π½ππ»π πΏπ»π°ππΈπ½πΆ ππΏπ»πΎπ°π³π΄π³ π±π @SNEHABHI_UPDATES**", reply_markup=BACK_BUTTON
        )
    else:
        callsmusic.pytgcalls.pause_stream(query.message.chat.id)
        await query.edit_message_text(
            "βΈ ππΎπ½πΆ π·π°π π±π΄π΄π½ π΄π½π³π΄π³  π±π @SNEHABHI_UPDATES", reply_markup=BACK_BUTTON
        )


@Client.on_callback_query(filters.regex("cbresume"))
@cb_admin_check
async def cbresume(_, query: CallbackQuery):
    get_chat_id(query.message.chat)
    if (query.message.chat.id not in callsmusic.pytgcalls.active_calls) or (
        callsmusic.pytgcalls.active_calls[query.message.chat.id] == "resumed"
    ):
        await query.edit_message_text(
            "β **π½πΎ πΌπππΈπ² πΈπ πΏπ°πππ΄π³  π±π @SNEHABHI_UPDATES**", reply_markup=BACK_BUTTON
        )
    else:
        callsmusic.pytgcalls.resume_stream(query.message.chat.id)
        await query.edit_message_text(
            "βΆοΈ πΌπππΈπ² π·π°π π±π΄π΄π½ ππ΄πππΌπ΄π³  π±π @SNEHABHI_UPDATES", reply_markup=BACK_BUTTON
        )


@Client.on_callback_query(filters.regex("cbend"))
@cb_admin_check
async def cbend(_, query: CallbackQuery):
    get_chat_id(query.message.chat)
    if query.message.chat.id not in callsmusic.pytgcalls.active_calls:
        await query.edit_message_text(
            "β **π½πΎ ππΎπ½πΆ πΈπ π²ππππ΄π½ππ»π πΏπ»π°ππΈπ½πΆ ππΏπ»πΎπ°π³π΄π³ π±π @SNEHABHI_UPDATES**", reply_markup=BACK_BUTTON
        )
    else:
        try:
            queues.clear(query.message.chat.id)
        except QueueEmpty:
            pass

        callsmusic.pytgcalls.leave_group_call(query.message.chat.id)
        await query.edit_message_text(
            "β ππ·π΄ πΌπππΈπ² πππ΄ππ΄ π·π°π π±π΄π΄π½ π²π»π΄π°ππ΄π³ π°π½π³ πππ²π²π΄ππ΅ππ»π»π π»π΄π΅π ππ² ππΏπ»πΎπ°π³π΄π³ π±π @SNEHABHI_UPDATES",
            reply_markup=BACK_BUTTON,
        )


@Client.on_callback_query(filters.regex("cbskip"))
@cb_admin_check
async def cbskip(_, query: CallbackQuery):
    global que
    chat_id = get_chat_id(query.message.chat)
    if query.message.chat.id not in callsmusic.pytgcalls.active_calls:
        await query.edit_message_text(
            "β **π½πΎ ππΎπ½πΆ πΈπ π²ππππ΄π½ππ»π πΏπ»π°ππΈπ½πΆ ππΏπ»πΎπ°π³π΄π³ π±π @SNEHABHI_UPDATES**", reply_markup=BACK_BUTTON
        )
    else:
        queues.task_done(query.message.chat.id)

        if queues.is_empty(query.message.chat.id):
            callsmusic.pytgcalls.leave_group_call(query.message.chat.id)
        else:
            callsmusic.pytgcalls.change_stream(
                query.message.chat.id, queues.get(query.message.chat.id)["file"]
            )

    qeue = que.get(chat_id)
    if qeue:
        qeue.pop(0)
    if not qeue:
        return
    await query.edit_message_text(
        "β­ **ππΎπ π·π°ππ΄ ππΊπΈπΏπΏπ΄π³ ππΎ ππ·π΄ π½π΄ππ ππΎπ½πΆ ππΏπ»πΎπ°π³π΄π³ π±π @SNEHABHI_UPDATES**", reply_markup=BACK_BUTTON
    )
