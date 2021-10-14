import logging
import pyrogram
from decouple import config
from os import system, listdir, remove

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

# vars
API_ID = config("API_ID", default=None, cast=int)
API_HASH = config("API_HASH", default=None)
BOT_TOKEN = config("BOT_TOKEN", default=None)

if __name__ == "__main__":
    print("Starting Bot...")
    here = listdir("./SauceBOT/")
    print(here)
    if "script.sh" in here:
        system("bash ./SauceBOT/script.sh")
        remove("./SauceBOT/script.sh")
    plugins = dict(root="SauceBOT/plugins")
    app = pyrogram.Client(
        "SauceBOT",
        bot_token=BOT_TOKEN,
        api_id=API_ID,
        api_hash=API_HASH,
        plugins=plugins
    )
    app.run()

