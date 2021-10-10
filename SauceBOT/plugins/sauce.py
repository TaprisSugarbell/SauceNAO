import os
import wget
from ..helper.NAO import nao
from ..helper.slk import short
from pyrogram import Client, filters
from ..helper.random_key import rankey
from ..helper.screenshot import screenshot
from pyrogram.types import InlineKeyboardMarkup, InputMediaPhoto


# Vars
# dt = None
file = None
cmnds = ["sauce", "salsa", "source"]


@Client.on_message(filters.command(cmnds) | filters.regex(r"([Ss][Aa][Uu][Cc][Ee]|"
                                                          r"[Ss][Aa][Ll][Ss][Aa])|"
                                                          r"[Ss][Oo][Uu][Rr][Cc][Ee]"))
async def __sauce__(bot, update):
    print(update)
    chat_id = update.chat.id
    reply_to_message = update.reply_to_message
    if reply_to_message:
        photo = reply_to_message.photo
        if photo:
            m = await bot.send_animation(chat_id,
                                         animation="https://tinyurl.com/ye8kuszs",
                                         caption="Buscando...",
                                         reply_to_message_id=update.message_id)
            dt = "../SauceBOT/downloads/" + str(update.from_user.id) + "/"
            file = await bot.download_media(photo.file_id, dt + rankey(8) + ".png")
            text, btns, urlnao_clean, google, similarity = nao(file)
            await bot.edit_message_caption(chat_id,
                                           m["message_id"],
                                           caption=text,
                                           reply_markup=InlineKeyboardMarkup(btns))
            if similarity > 45:
                sc = screenshot(short(urlnao_clean))
            else:
                sc = screenshot(short(google))
            print(sc)
            f = wget.download(sc, "".join(dt[3:] + rankey(8) + ".png"))
            await bot.edit_message_media(chat_id,
                                         message_id=m["message_id"],
                                         media=InputMediaPhoto(f))
            # await bot.send_message(chat_id,
            #                        text,
            #                        reply_markup=InlineKeyboardMarkup(btns))

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
