import json
from urllib.parse import urlencode
import random
import htmlwebshot
import imgbbpy
import requests
from decouple import config

IMGBB_API = config("IMGBB_API", default=None)


def status200(rq):
    if rq.status_code != 200:
        raise Exception("screenshot failed", rq.status_code, rq.content.decode())
    elif rq.json()["error"]:
        raise Exception("screenshot failed", rq.status_code, rq.json()["error"])


def upload_img(url=None, file=None, name="image", expiration=None):
    client = imgbbpy.SyncClient(IMGBB_API)
    image = client.upload(url=url, file=file, name=name, expiration=expiration)
    return image


def shotscreen(link=None, mode=0, width=1920, height=1080):
    RN = "https://render-tron.appspot.com/screenshot/"
    SCREENSHOT_API = config("SCREENSHOT_API", default=None)
    if mode == 0:
        try:
            params = urlencode(dict(access_key=SCREENSHOT_API,
                                    format="png",
                                    response_type="json",
                                    no_cookie_banners=True,
                                    no_tracking=True,
                                    url=link
                                    )
                               )
            r = requests.get("https://api.apiflash.com/v1/urltoimage", params=params)
            # status200(r)
            sc = r.json()["url"]
        except json.decoder.JSONDecodeError:
            params = {"width": width,
                      "height": height}
            r = requests.get(RN + link, params=params)
            sc = r.url
        return sc
    elif mode == 1:
        params = {"width": width,
                  "height": height}
        r = requests.get(RN + link, params=params)
        sc = r.url
        return sc
    else:
        raise Exception("This mode no exist", mode, "only mode 0 and 1")


# async def screenshot(link, width=1920, height=1080):
#     # return f"http://api.s-shot.ru/{width}x{height}/PNG/{width}/Z100/?{quote_plus(link)}"
#     return f"http://api.s-shot.ru/{width}x{height}/PNG/{width}/Z100/?{quote_plus(link)}"

async def screenshot(link, output=None):
    cn = htmlwebshot.WebShot(quality=70,
                             flags=["--enable-javascript", "--no-stop-slow-scripts"],
                             delay=random.randint(3, 4),
                             size=(1080, 1920))
                             # size=(1620, 1920))
    return await cn.create_pic_async(url=link, output=output)
