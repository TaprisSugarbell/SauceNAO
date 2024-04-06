import pyrogram.errors
from ..helper.mongo_connect import *
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Vars
u = Mongo(URI, "SauceBOT", "users")


@Client.on_callback_query(filters.regex(r"^config"))
async def __config__(bot, update):
    print(update)
    callcack_query_id = update.id
    chat_id = update.message.chat.id
    user_id = update.from_user.id
    message_id = update.message.id
    btns = [
        [
            InlineKeyboardButton("Sitios", "sites"),
            InlineKeyboardButton("Media", "upload_config")
        ],
        [
            InlineKeyboardButton("Tiempo de Links", "time")
        ]
    ]
    try:
        await bot.edit_message_reply_markup(chat_id,
                                            message_id,
                                            reply_markup=InlineKeyboardMarkup(btns))
    except pyrogram.errors.exceptions.bad_request_400.MessageNotModified:
        await bot.answer_callback_query(callcack_query_id,
                                        "No se pudo modificar el mensaje por un error en el bot.",
                                        show_alert=True)


@Client.on_callback_query(filters.regex(r"upload_config"))
async def __upconfig__(bot, update):
    print(update)
    yes = "✅"
    non = "❌"
    poss = ["photo", "document"]
    callcack_query_id = update.id
    user_id = update.from_user.id
    chat_id = update.message.chat.id
    text = update.data.split("_")[-1]
    message_id = update.message.id
    c = await confirm(u, {"user_id": user_id})
    if c:
        try:
            upload_config = c[0]["upload_config"]
            if upload_config != text:
                upload_config = text
            else:
                upload_config = "document"
            await update_(u, {"user_id": user_id}, {"upload_config": upload_config})
        except KeyError:
            if text in poss:
                upload_config = text
            else:
                upload_config = "document"
            await update_(u, {"user_id": user_id}, {"upload_config": upload_config})
    else:
        if text in poss:
            upload_config = text
        else:
            upload_config = "document"
        await add_(u, {"user_id": user_id,
                       "SauceNAO_API": None,
                       "upload_config": upload_config})
    if upload_config == "photo":
        emf = yes
        emn = non
    else:
        emf = non
        emn = yes
    btns = [
        [
            InlineKeyboardButton(f"Photo {emf}", "upload_config_photo"),
            InlineKeyboardButton(f"Document {emn}", "upload_config_document")
        ],
        [
            InlineKeyboardButton("Atrás", "config")
        ]
    ]
    try:
        await bot.edit_message_reply_markup(chat_id or user_id,
                                            message_id,
                                            reply_markup=InlineKeyboardMarkup(btns))
    except pyrogram.errors.exceptions.bad_request_400.MessageNotModified:
        await bot.answer_callback_query(callcack_query_id,
                                        f"{text.capitalize()} {emn} ya esta marcada, no puedes elegir la misma opción.",
                                        show_alert=True)




