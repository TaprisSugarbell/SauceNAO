import os
import wget
import random
from ..helper.NAO import nao
from ..helper.slk import short
from pyrogram import Client, filters
from ..helper.random_key import rankey
from ..helper.magic_funcs import notNone
from ..helper.screenshot import screenshot
from pyrogram.types import InlineKeyboardMarkup, InputMediaPhoto


# Vars
# dt = None
file = None
cmnds = ["sauce", "salsa", "source", "fuente", "name", "soup"]


@Client.on_message(filters.command(cmnds) |
                   (filters.regex(r"([Ss][Aa][Uu][Cc][Ee]|"
                                  r"[Ss][Aa][Ll][Ss][Aa])|"
                                  r"[Ss][Oo][Uu][Rr][Cc][Ee]|"
                                  r"[Ff][Uu][Ee][Nn][Tt][Ee]|"
                                  r"[Nn][Aa][Mm][Ee]|"
                                  r"[Ss][Oo][Uu][Pp]")
                    & ~filters.bot & ~filters.channel & ~filters.group)|
                   (filters.photo & filters.private))
async def __sauce__(bot, update):
    print(update)
    chat_id = update.chat.id
    reply_to_message = update.reply_to_message
    forward_from = update.forward_from
    photo = update.photo
    if reply_to_message and "".join(update.text.split("/")).lower() in cmnds or forward_from or photo:
        photo = notNone(reply_to_message, forward_from, update)
        if photo:
            m = await bot.send_animation(chat_id,
                                         animation="https://tinyurl.com/ye8kuszs",
                                         caption="Buscando...",
                                         reply_to_message_id=update.message_id)
            dt = "../SauceBOT/downloads/" + str(update.from_user.id) + "/"
            file = await bot.download_media(photo, dt + rankey(8) + ".png")
            text, btns, urlnao_clean, google, similarity = nao(file, user_id=update.from_user.id)
            try:
                await bot.edit_message_caption(chat_id,
                                               m["message_id"],
                                               caption=text,
                                               reply_markup=InlineKeyboardMarkup(btns))
            except Exception as e:
                print(e)
            if similarity > 60 and random.randint(0, 30) == 30:
                sc = screenshot(short(urlnao_clean))
            else:
                sc = screenshot(short(google))
            print(sc)
            f = wget.download(sc, "".join(dt[3:] + rankey(8) + ".png"))
            try:
                await bot.edit_message_media(chat_id,
                                             message_id=m["message_id"],
                                             media=InputMediaPhoto(f,
                                                                   caption=text),
                                             reply_markup=InlineKeyboardMarkup(btns))
            except Exception as e:
                print(e)
            try:
                if file is not None:
                    try:
                        # os.remove("".join(dt[3:] + file.split("/")[-1]))
                        os.remove(file)
                    except Exception as e:
                        print(e)
                    try:
                        os.remove(f)
                    except Exception as e:
                        print(e)
                # print(os.getcwd())
                # rmtree("".join(dt[3:]))
            except Exception as e:
                print(e)
