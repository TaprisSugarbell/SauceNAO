import re
from ..helper.mongo_connect import *
from pyrogram import Client, filters

# Vars
u = Mongo(URI, "SauceBOT", "users")


@Client.on_message(filters.command(["api"]) & filters.private)
async def __api__(bot, update):
    print(update)
    chat_id = update.chat.id
    user_id = update.from_user.id
    text = update.text.split()[-1]
    SAUCE_API = re.sub(r"[^a-zA-Z0-9]", "", text)
    c = await confirm(u, {"user_id": user_id})
    if c:
        await update_(u,
                      {"user_id": user_id},
                      {"SAUCE_API": SAUCE_API})
        await bot.send_message(chat_id,
                               "Tu API se ha actualizado con éxito.")
    else:
        await add_(u,
                   {"user_id": user_id,
                    "SAUCE_API": SAUCE_API})
        await bot.send_message(chat_id,
                               "Se ha agregado tu API.")

