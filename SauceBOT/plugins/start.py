from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


@Client.on_message(filters.command(["start"]))
async def __start__(bot, update):
    print(update)
    chat_id = update.chat.id
    await bot.send_message(chat_id,
                           "Hola, soy **SalsaNAOBot**\n"
                           "el mejor Reverse Image Search de Telegram, si deseas"
                           "buscar una imagen en SauceNAO debes ingresar tu "
                           "[api_key](https://saucenao.com/user.php?page=search-api) "
                           "si no te has registrado en el sitio debes hacerlo pero el bot"
                           "funcionara solo que sin darte información buscando en sitios como:\n"
                           "Google, IQDB, Yandex.\n"
                           "Para más información puedes ver el comando /help o @SauceNAO")


@Client.on_message(filters.command(["help"]))
async def __help__(bot, update):
    print(update)
    chat_id = update.chat.id
    await bot.send_message(chat_id,
                           "[Info](https://telegra.ph/Info-10-15-2)",
                           reply_markup=InlineKeyboardMarkup(
                               [
                                   [
                                       InlineKeyboardButton("Config", "config")
                                   ]
                               ]
                           ))



