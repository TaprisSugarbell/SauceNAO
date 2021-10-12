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


@Client.on_message(filters.photo & filters.private)
async def __sauce__(bot, update):
    print(update)
    photo = update.photo
    chat_id = update.chat.id
    forward_from = update.forward_from
    reply_to_message = update.reply_to_message
    if forward_from or photo:
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
                user_id = forward_from.id
                dt = "../SauceBOT/downloads/" + str(user_id) + "/"
            #     await bot.delete_messages(chat_id,
            #                               message_ids=m["message_id"])
            file = await bot.download_media(photo, dt + rankey(8) + ".png")
            text, btns, urlnao_clean, google, similarity = nao(file, user_id=user_id)
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

