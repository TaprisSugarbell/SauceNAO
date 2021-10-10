import os
import wget
from ..helper.NAO import nao
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InputMediaPhoto


# Vars
# dt = None
file = None


@Client.on_message(filters.command(["sauce", "salsa", "source"]) | filters.regex(r"(sauce|salsa|source)"))
async def __sauce__(bot, update):
    print(update)
    chat_id = update.chat.id
    reply_to_message = update.reply_to_message
    if reply_to_message:
        photo = reply_to_message.photo
        if photo:
            m = await bot.send_animation(chat_id,
                                         animation="https://tinyurl.com/ye8kuszs",
                                         caption="Buscando...")
            dt = "../SauceBOT/downloads/" + str(update.from_user.id) + "/"
            file = await bot.download_media(photo.file_id, dt)
            text, btns, screenshot = nao(file)
            f = wget.download(screenshot, "".join(dt[3:] + "file.png"))
            await bot.edit_message_media(chat_id,
                                         message_id=m["message_id"],
                                         media=InputMediaPhoto(
                                             f,
                                             caption=text
                                         ),
                                         reply_markup=InlineKeyboardMarkup(btns))
            # await bot.send_message(chat_id,
            #                        text,
            #                        reply_markup=InlineKeyboardMarkup(btns))

    try:
        if file is not None:
            try:
                os.remove("".join(dt[3:] + file.split("/")[-1]))
                # os.remove(file)
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
