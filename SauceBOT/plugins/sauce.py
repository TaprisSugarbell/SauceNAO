import os
import wget
import random
from time import sleep
from ..helper.NAO import nao
from ..helper.slk import short
from pyrogram import Client, filters
from ..helper.mongo_connect import *
from ..helper.random_key import rankey
from ..helper.magic_funcs import notNone
from ..helper.screenshot import screenshot, shotscreen
from pyrogram.types import InlineKeyboardMarkup, InputMediaPhoto, InputMediaDocument

# Vars
# dt = None
u = Mongo(URI, "SauceBOT", "users")
file = None
cmnds = ["sauce", "salsa", "source", "fuente", "name", "soup"]


@Client.on_message(filters.command(cmnds) |
                   (filters.regex(r"([Ss][Aa][Uu][Cc][Ee]|"
                                  r"[Ss][Aa][Ll][Ss][Aa])|"
                                  r"[Ss][Oo][Uu][Rr][Cc][Ee]|"
                                  r"[Ff][Uu][Ee][Nn][Tt][Ee]|"
                                  r"[Nn][Aa][Mm][Ee]|"
                                  r"[Ss][Oo][Uu][Pp]") & filters.reply))
async def __sauce__(bot, update):
    async def upload_command(id_of_chat, method=bot.edit_message_media, **kwargs):
        await method(chat_id=id_of_chat, **kwargs)

    print(update)
    chat_id = update.chat.id
    try:
        user_id = update.from_user.id
    except Exception as e:
        print(e)
        user_id = None
    forward_from = update.forward_from
    reply_to_message = update.reply_to_message
    if reply_to_message and "".join(update.text.split("/")).lower() in cmnds:
        photo = notNone(reply_to_message, update)
        if photo:
            m = await bot.send_animation(chat_id,
                                         animation="https://tinyurl.com/ye8kuszs",
                                         caption="Buscando...",
                                         reply_to_message_id=update.message_id)
            try:
                user_id = update.from_user.id
                dt = "../SauceBOT/downloads/" + str(user_id) + "/"
            except Exception as e:
                print(e)
                try:
                    user_id = forward_from.id
                except AttributeError:
                    user_id = chat_id
                dt = "../SauceBOT/downloads/" + str(user_id) + "/"
            #     await bot.delete_messages(chat_id,
            #                               message_ids=m["message_id"])
            file = await bot.download_media(photo, dt + rankey(8) + ".png")
            text, btns, (urlnao_clean, google, yandex), similarity = nao(file, user_id=user_id)
            try:
                await bot.edit_message_caption(chat_id,
                                               m["message_id"],
                                               caption=text,
                                               reply_markup=InlineKeyboardMarkup(btns))
            except Exception as e:
                print(e)
            dig = random.randint(0, 30)
            if similarity > 60 and dig == 30:
                try:
                    f = await screenshot(short(urlnao_clean), height=1620)
                except Exception as e:
                    print(e)
                    sc = shotscreen(short(urlnao_clean), height=1620)
                    f = wget.download(sc, "".join(dt[3:] + rankey(8) + ".png"))
            else:
                if dig > 20:
                    try:
                        f = await screenshot(short(yandex), height=1620)
                    except Exception as e:
                        print(e)
                        sc = shotscreen(short(yandex), height=1620)
                        f = wget.download(sc, "".join(dt[3:] + rankey(8) + ".png"))
                else:
                    try:
                        sc = shotscreen(short(google), height=1620)
                        f = wget.download(sc, "".join(dt[3:] + rankey(8) + ".png"))
                    except Exception as e:
                        print(e)
                        sc = shotscreen(short(google), height=1620)
                        f = wget.download(sc, "".join(dt[3:] + rankey(8) + ".png"))

            print(f)
            try:
                if user_id:
                    c = await confirm(u, {"user_id": user_id})
                    if c:
                        try:
                            upload_config = c[0]["upload_config"]
                        except KeyError:
                            await update_(u, {"user_id": user_id}, {"upload_config": "document"})
                            upload_config = "document"
                        if upload_config == "document":
                            await upload_command(chat_id,
                                                 message_id=m["message_id"],
                                                 media=InputMediaDocument(f,
                                                                          caption=text),
                                                 reply_markup=InlineKeyboardMarkup(btns))
                        else:
                            await upload_command(chat_id,
                                                 message_id=m["message_id"],
                                                 media=InputMediaPhoto(f,
                                                                       caption=text),
                                                 reply_markup=InlineKeyboardMarkup(btns))
                    else:
                        await upload_command(chat_id,
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
                    # if "https" not in f:
                    try:
                        os.remove(f)
                    except FileNotFoundError:
                        pass
                    except Exception as e:
                        print(e)
                # print(os.getcwd())
                # rmtree("".join(dt[3:]))
            except Exception as e:
                print(e)
