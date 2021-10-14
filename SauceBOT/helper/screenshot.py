import json
import imgbbpy
import requests
import htmlwebshot
from decouple import config
from urllib.parse import urlencode, quote_plus


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


def shotscreen(link=None):
    RN = "https://render-tron.appspot.com/screenshot/"
    SCREENSHOT_API = config("SCREENSHOT_API", default=None)
    try:
        params = urlencode(dict(access_key=SCREENSHOT_API,
                                format="jpeg",
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
        params = {"width": 1920,
                  "height": 1080}
        r = requests.get(RN + link, params=params)
        sc = r.url
    return sc


async def screenshot(link, output=None):
    cn = htmlwebshot.WebShot(quality=88,
                             flags=["--enable-javascript", "--no-stop-slow-scripts"],
                             delay=10,
                             size=(1080, 1920))
    return await cn.create_pic_async(url=link, output=output)



