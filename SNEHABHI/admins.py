from asyncio import QueueEmpty

from callsmusic import callsmusic
from callsmusic.queues import queues
from config import BOT_USERNAME, que
from cache.admins import admins
from handlers.play import cb_admin_check
from helpers.channelmusic import get_chat_id
from helpers.dbtools import delcmd_is_on, delcmd_off, delcmd_on, handle_user_status
from helpers.decorators import authorized_users_only, errors
from helpers.filters import command, other_filters
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
    [[InlineKeyboardButton("🔙 Go Back", callback_data="cbback")]]
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
        "✅ Bot **𝚁𝙴𝙻𝙾𝙰𝙳𝙴𝙳 𝙲𝙾𝚁𝚁𝙴𝙲𝚃𝙻𝚈 𝚂𝙽𝙴𝙷𝙰𝙱𝙷𝙸 𝙱𝙾𝚃𝚉 !**\n✅ **𝙰𝙳𝙼𝙸𝙻𝙸𝚂𝚃** 𝙷𝙰𝚂 𝙱𝙴𝙴𝙽 **𝚄𝙿𝙳𝙰𝚃𝙴𝙳 𝙱𝚈 @SNEHABHI_UPDATES !**"
    )


# Control Menu Of Player
@Client.on_message(command(["control", f"control@{BOT_USERNAME}"]) & other_filters)
@errors
@authorized_users_only
async def controlset(_, message: Message):
    await message.reply_text(
        "💡 **𝙷𝙴𝚁𝙴 𝙸𝚂 𝚃𝙷𝙴 𝙼𝙴𝙽𝚄 𝙲𝙾𝙽𝚃𝚁𝙾𝙻 𝙾𝙵 𝙱𝙾𝚃 :**",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("⏸ pause", callback_data="cbpause"),
                    InlineKeyboardButton("▶️ resume", callback_data="cbresume"),
                ],
                [
                    InlineKeyboardButton("⏩ skip", callback_data="cbskip"),
                    InlineKeyboardButton("⏹ stop", callback_data="cbend"),
                ],
                [InlineKeyboardButton("⛔ anti cmd", callback_data="cbdelcmds")],
                [InlineKeyboardButton("🗑 Close", callback_data="close")],
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
        await message.reply_text("❌ **𝙽𝙾 𝙼𝚄𝚂𝙸𝙲 𝙸𝚂 𝙲𝚄𝚁𝚁𝙴𝙽𝚃𝙻𝚈 𝙿𝙻𝙰𝚈𝙸𝙽𝙶 𝚄𝙿𝙻𝙾𝙰𝙳𝙴𝙳 𝙱𝚈 @SNEHABHI_UPDATES**")
    else:
        callsmusic.pytgcalls.pause_stream(chat_id)
        await message.reply_text(
            "⏸ **Track paused.**\n\n• **𝚃𝙾 𝚁𝙴𝚂𝚄𝙼𝙴 𝚃𝙷𝙴 𝚂𝙾𝙽𝙶 , 𝚄𝚂𝙴 𝚃𝙷𝙴**\n» `/resume` 𝙲𝙾𝙼𝙼𝙰𝙽𝙳 𝚄𝙿𝙻𝙾𝙰𝙳𝙴𝙳 𝙱𝚈 @SNEHABHI_UPDATES."
        )


@Client.on_message(command(["resume", f"resume@{BOT_USERNAME}"]) & other_filters)
@errors
@authorized_users_only
async def resume(_, message: Message):
    chat_id = get_chat_id(message.chat)
    if (chat_id not in callsmusic.pytgcalls.active_calls) or (
        callsmusic.pytgcalls.active_calls[chat_id] == "playing"
    ):
        await message.reply_text("❌ **𝙽𝙾 𝙼𝚄𝚂𝙸𝙲 𝙸𝚂 𝙿𝙰𝚄𝚂𝙴𝙳 𝚄𝙿𝙻𝙾𝙰𝙳𝙴𝙳 𝙱𝚈 @SNEHABHI_UPDATES**")
    else:
        callsmusic.pytgcalls.resume_stream(chat_id)
        await message.reply_text(
            "▶️ **Track resumed.**\n\n• **𝚃𝙾 𝙿𝙰𝚄𝚂𝙴 𝚃𝙷𝙴 𝚂𝙾𝙽𝙶 , 𝚄𝚂𝙴 𝚃𝙷𝙴**\n» `/pause` 𝙲𝙾𝙼𝙼𝙰𝙽𝙳 𝚄𝙿𝙻𝙾𝙰𝙳𝙴𝙳 𝙱𝚈 @SNEHABHI_UPDATES."
        )


@Client.on_message(command(["end", f"end@{BOT_USERNAME}"]) & other_filters)
@errors
@authorized_users_only
async def stop(_, message: Message):
    chat_id = get_chat_id(message.chat)
    if chat_id not in callsmusic.pytgcalls.active_calls:
        await message.reply_text("❌ **𝙽𝙾 𝙼𝚄𝚂𝙸𝙲 𝙸𝚂 𝙲𝚄𝚁𝚁𝙴𝙽𝚃𝙻𝚈 𝙿𝙻𝙰𝚈𝙸𝙽𝙶 𝚄𝙿𝙻𝙾𝙰𝙳𝙴𝙳 𝙱𝚈 @SNEHABHI_UPDATES**")
    else:
        try:
            queues.clear(chat_id)
        except QueueEmpty:
            pass

        callsmusic.pytgcalls.leave_group_call(chat_id)
        await message.reply_text("✅ **𝙼𝚄𝚂𝙸𝙲 𝚂𝙾𝙽𝙶 𝙷𝙰𝚂 𝙴𝙽𝙳𝙴𝙳 𝚄𝙿𝙻𝙾𝙰𝙳𝙴𝙳 𝙱𝚈 @SNEHABHI_UPDATES**")


@Client.on_message(command(["skip", f"skip@{BOT_USERNAME}"]) & other_filters)
@errors
@authorized_users_only
async def skip(_, message: Message):
    global que
    chat_id = get_chat_id(message.chat)
    if chat_id not in callsmusic.pytgcalls.active_calls:
        await message.reply_text("❌ **𝙽𝙾 𝙼𝚄𝚂𝙸𝙲 𝙸𝚂 𝙲𝚄𝚁𝚁𝙴𝙽𝚃𝙻𝚈 𝙿𝙻𝙰𝚈𝙸𝙽𝙶 𝚄𝙿𝙻𝙾𝙰𝙳𝙴𝙳 𝙱𝚈 @SNEHABHI_UPDATES**")
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
    await message.reply_text("⏭ **𝚈𝙾𝚄'𝚅𝙴 𝚂𝙺𝙸𝙿𝙿𝙴𝙳 𝚃𝙾 𝚃𝙷𝙴 𝙽𝙴𝚇𝚃 𝚂𝙾𝙽𝙶 𝙱𝚈 @SNEHABHI_UPDATES.**")


@Client.on_message(command(["auth", f"auth@{BOT_USERNAME}"]) & other_filters)
@authorized_users_only
async def authenticate(client, message):
    global admins
    if not message.reply_to_message:
        return await message.reply("💡 𝚁𝙴𝙿𝙻𝚈 𝚃𝙾 𝙼𝚂𝙶 𝚃𝙾 𝙰𝚄𝚃𝙷𝙾𝚁𝙸𝚉𝙴 𝚄𝚂𝙴𝚁 !")
    if message.reply_to_message.from_user.id not in admins[message.chat.id]:
        new_admins = admins[message.chat.id]
        new_admins.append(message.reply_to_message.from_user.id)
        admins[message.chat.id] = new_admins
        await message.reply(
            "🟢 user authorized.\n\n𝙵𝚁𝙾𝙼 𝙽𝙾𝚆 𝚃𝙷𝙰𝚃'𝚂 𝚄𝚂𝙴𝚁 𝙲𝙰𝙽 𝚄𝚂𝙴 𝚃𝙷𝙴 𝙰𝙳𝙼𝙸𝙽 𝙲𝙾𝙼𝙼𝙰𝙽𝙳 𝚄𝙿𝙻𝙾𝙰𝙳𝙴𝙳 𝙱𝚈 @SNEHABHI_UPDATES."
        )
    else:
        await message.reply("✅ 𝚄𝚂𝙴R 𝙰𝙻𝚁𝙴𝙰𝙳𝚈 𝙰𝚄𝚃𝙷𝙾𝚁𝙸𝚉𝙴𝙳! 𝚄𝙿𝙻𝙾𝙰𝙳𝙴𝙳 𝙱𝚈 @SNEHABHI_UPDATES")


@Client.on_message(command(["deauth", f"deauth@{BOT_USERNAME}"]) & other_filters)
@authorized_users_only
async def deautenticate(client, message):
    global admins
    if not message.reply_to_message:
        return await message.reply("💡 𝚁𝙴𝙿𝙻𝚈 𝚃𝙾 𝙼𝚂𝙶 𝚃𝙾 𝙳𝙴𝙰𝚄𝚃𝙷𝙾𝚁𝙸𝚉𝙴 𝚄𝚂𝙴𝚁 !")
    if message.reply_to_message.from_user.id in admins[message.chat.id]:
        new_admins = admins[message.chat.id]
        new_admins.remove(message.reply_to_message.from_user.id)
        admins[message.chat.id] = new_admins
        await message.reply(
            "🔴 𝚄𝚂𝙴𝚁 𝙳𝙴𝙰𝚄𝚃𝙷𝙾𝚁𝙸𝚉𝙴𝙳.\n\n𝙵𝚁𝙾𝙼 𝙽𝙾𝚆 𝚃𝙷𝙰𝚃'𝚂 𝚄𝚂𝙴𝚁 𝙲𝙰𝙽'𝚃 𝚄𝚂𝙴 𝚃𝙷𝙴 𝙰𝙳𝙼𝙸𝙽 𝙲𝙾𝙼𝙼𝙰𝙽𝙳 𝚄𝙿𝙻𝙾𝙰𝙳𝙴𝙳 𝙱𝚈 @SNEHABHI_UPDATES."
        )
    else:
        await message.reply("✅ 𝚄𝚂𝙴R 𝙰𝙻𝚁𝙴𝙰𝙳𝚈 𝙳𝙴𝙰𝚄𝚃𝙷𝙾𝚁𝙸𝚉𝙴𝙳! 𝚄𝙿𝙻𝙾𝙰𝙳𝙴𝙳 𝙱𝚈 @SNEHABHI_UPDATES")


# this is a anti cmd feature
@Client.on_message(command(["delcmd", f"delcmd@{BOT_USERNAME}"]) & other_filters)
@authorized_users_only
async def delcmdc(_, message: Message):
    if len(message.command) != 2:
        return await message.reply_text(
            "𝚁𝙴𝙰𝙳 𝚃𝙷𝙴 /help 𝙼𝚂𝙶 𝚃𝙾 𝙺𝙽𝙾𝚆 𝙷𝙾𝚆 𝚃𝙾 𝚄𝚂𝙴 𝚃𝙷𝙸𝚂 𝙲𝙾𝙼𝙼𝙰𝙽𝙳 𝚄𝙿𝙻𝙾𝙰𝙳𝙴𝙳 𝙱𝚈 @SNEHABHI_UPDATES"
        )
    status = message.text.split(None, 1)[1].strip()
    status = status.lower()
    chat_id = message.chat.id
    if status == "on":
        if await delcmd_is_on(message.chat.id):
            return await message.reply_text("✅ 𝙰𝙻𝚁𝙴𝙰𝙳𝚈 𝙰𝙲𝚃𝙸𝚅𝙰𝚃𝙴𝙳 𝚄𝙿𝙻𝙾𝙰𝙳𝙴𝙳 𝙱𝚈 @SNEHABHI_UPDATES")
        await delcmd_on(chat_id)
        await message.reply_text("🟢 𝙰𝙲𝚃𝙸𝚅𝙰𝚃𝙴D 𝚂𝚄𝙲𝙲𝙴𝚂𝚂𝙵𝚄𝙻𝙻𝚈  𝙱𝚈 @SNEHABHI_UPDATES")
    elif status == "off":
        await delcmd_off(chat_id)
        await message.reply_text("🔴 𝙳𝙸𝚂𝙰𝙱𝙻𝙴𝙳 𝚂𝚄𝙲𝙲𝙴𝚂𝚂𝙵𝚄𝙻𝙻𝚈  𝙱𝚈 @SNEHABHI_UPDATES")
    else:
        await message.reply_text(
            "𝚁𝙴𝙰𝙳 𝚃𝙷𝙴 /help 𝙼𝚂𝙶 𝚃𝙾 𝙺𝙽𝙾𝚆 𝙷𝙾𝚆 𝚃𝙾 𝚄𝚂𝙴 𝚃𝙷𝙸𝚂 𝙲𝙾𝙼𝙼𝙰𝙽𝙳 𝚄𝙿𝙻𝙾𝙰𝙳𝙴𝙳 𝙱𝚈 @SNEHABHI_UPDATES"
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
            "❌ **𝙽𝙾 𝚂𝙾𝙽𝙶 𝙸𝚂 𝙲𝚄𝚁𝚁𝙴𝙽𝚃𝙻𝚈 𝙿𝙻𝙰𝚈𝙸𝙽𝙶 𝚄𝙿𝙻𝙾𝙰𝙳𝙴𝙳 𝙱𝚈 @SNEHABHI_UPDATES**", reply_markup=BACK_BUTTON
        )
    else:
        callsmusic.pytgcalls.pause_stream(query.message.chat.id)
        await query.edit_message_text(
            "⏸ 𝚂𝙾𝙽𝙶 𝙷𝙰𝚂 𝙱𝙴𝙴𝙽 𝙴𝙽𝙳𝙴𝙳  𝙱𝚈 @SNEHABHI_UPDATES", reply_markup=BACK_BUTTON
        )


@Client.on_callback_query(filters.regex("cbresume"))
@cb_admin_check
async def cbresume(_, query: CallbackQuery):
    get_chat_id(query.message.chat)
    if (query.message.chat.id not in callsmusic.pytgcalls.active_calls) or (
        callsmusic.pytgcalls.active_calls[query.message.chat.id] == "resumed"
    ):
        await query.edit_message_text(
            "❌ **𝙽𝙾 𝙼𝚄𝚂𝙸𝙲 𝙸𝚂 𝙿𝙰𝚄𝚂𝙴𝙳  𝙱𝚈 @SNEHABHI_UPDATES**", reply_markup=BACK_BUTTON
        )
    else:
        callsmusic.pytgcalls.resume_stream(query.message.chat.id)
        await query.edit_message_text(
            "▶️ 𝙼𝚄𝚂𝙸𝙲 𝙷𝙰𝚂 𝙱𝙴𝙴𝙽 𝚁𝙴𝚂𝚄𝙼𝙴𝙳  𝙱𝚈 @SNEHABHI_UPDATES", reply_markup=BACK_BUTTON
        )


@Client.on_callback_query(filters.regex("cbend"))
@cb_admin_check
async def cbend(_, query: CallbackQuery):
    get_chat_id(query.message.chat)
    if query.message.chat.id not in callsmusic.pytgcalls.active_calls:
        await query.edit_message_text(
            "❌ **𝙽𝙾 𝚂𝙾𝙽𝙶 𝙸𝚂 𝙲𝚄𝚁𝚁𝙴𝙽𝚃𝙻𝚈 𝙿𝙻𝙰𝚈𝙸𝙽𝙶 𝚄𝙿𝙻𝙾𝙰𝙳𝙴𝙳 𝙱𝚈 @SNEHABHI_UPDATES**", reply_markup=BACK_BUTTON
        )
    else:
        try:
            queues.clear(query.message.chat.id)
        except QueueEmpty:
            pass

        callsmusic.pytgcalls.leave_group_call(query.message.chat.id)
        await query.edit_message_text(
            "✅ 𝚃𝙷𝙴 𝙼𝚄𝚂𝙸𝙲 𝚀𝚄𝙴𝚄𝙴 𝙷𝙰𝚂 𝙱𝙴𝙴𝙽 𝙲𝙻𝙴𝙰𝚁𝙴𝙳 𝙰𝙽𝙳 𝚂𝚄𝙲𝙲𝙴𝚂𝙵𝚄𝙻𝙻𝚈 𝙻𝙴𝙵𝚃 𝚅𝙲 𝚄𝙿𝙻𝙾𝙰𝙳𝙴𝙳 𝙱𝚈 @SNEHABHI_UPDATES",
            reply_markup=BACK_BUTTON,
        )


@Client.on_callback_query(filters.regex("cbskip"))
@cb_admin_check
async def cbskip(_, query: CallbackQuery):
    global que
    chat_id = get_chat_id(query.message.chat)
    if query.message.chat.id not in callsmusic.pytgcalls.active_calls:
        await query.edit_message_text(
            "❌ **𝙽𝙾 𝚂𝙾𝙽𝙶 𝙸𝚂 𝙲𝚄𝚁𝚁𝙴𝙽𝚃𝙻𝚈 𝙿𝙻𝙰𝚈𝙸𝙽𝙶 𝚄𝙿𝙻𝙾𝙰𝙳𝙴𝙳 𝙱𝚈 @SNEHABHI_UPDATES**", reply_markup=BACK_BUTTON
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
        "⏭ **𝚈𝙾𝚄 𝙷𝙰𝚅𝙴 𝚂𝙺𝙸𝙿𝙿𝙴𝙳 𝚃𝙾 𝚃𝙷𝙴 𝙽𝙴𝚇𝚃 𝚂𝙾𝙽𝙶 𝚄𝙿𝙻𝙾𝙰𝙳𝙴𝙳 𝙱𝚈 @SNEHABHI_UPDATES**", reply_markup=BACK_BUTTON
    )
