import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from pymongo import MongoClient
from config import BOT_USERNAME, DATABASE_URL as db_url
from SNEHABHI.SNEHUABHI.filters import command, other_filters
from SNEHABHI.SNEHUABHI.decorators import sudo_users_only

users_db = MongoClient(db_url)['users']
col = users_db['USER']
grps = users_db['GROUPS']


@Client.on_message(command(["gstats", f"gstats@{BOT_USERNAME}"]) & filters.private & ~filters.edited)
@sudo_users_only
async def stats(_, m: Message):
  users = col.find({})
  mfs = []
  for x in users:
    mfs.append(x['user_id'])
    
  total = len(mfs)
  
  grp = grps.find({})
  grps_ = []
  for x in grp:
    grps_.append(x['chat_id'])
    
  total_ = len(grps_)
  
  await m.reply_text(f"š„ Total Users: `{total}`\nš­ Total Groups: `{total_}`")
