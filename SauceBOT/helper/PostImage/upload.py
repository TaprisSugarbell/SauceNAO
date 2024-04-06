import re
import json
import time
import math
import requests
import datetime
# import lxml.html
import omnitools
from bs4 import BeautifulSoup
from multiprocessing.pool import ThreadPool
from decouple import config

__ALL__ = ["upload"]

postimages_domain = "https://postimages.org"

IMGBB_API = config("IMGBB", default=None)

# def donw(link):
#     b = BeautifulSoup(s.get(link).content, "html.parser")
#     return b.find("a", attrs={"id": "download"}).get("href").replace("?dl=1", "")


# def get_album(album):
#     rs = re.search("embed_value=.*};", album.text)
#     if rs:
#         r_S = rs[0].replace("embed_value=", "").replace(";", "")
#         dv = dict(json.loads(r_S))
#         d = {}
#         for i in dv:
#             d[int(dv[i][0])] = "https://postimg.cc/{}".format(i)
#         sorted_d = sorted(d.items())
#         return [o[1] for o in sorted_d]
#     else:
#         soup = BeautifulSoup(album.content, "html.parser")
#         controls = soup.find("div", attrs={"class": "controls"})
#         return ["https://postimg.cc/{}".format(controls.get("data-image"))]


def upload(image):
    api = "https://api.imgbb.com/1/upload"
    response = requests.post(
        api,
        files={
            "image": open(image, "rb")
        },
        params={
            "key": IMGBB_API,
            "expiration": 1800
        }
    ).json()
    return response["data"]["url"]
    # global s
    # if isinstance(urls, str):
    #     urls = [urls]
    # session_upload = str(math.floor(time.time() * 1000))
    # timestamp = datetime.datetime.now().strftime("%m/%d/%Y, %I:%M:%S %p")
    # s = requests.Session()
    # r = s.get(postimages_domain + "/web")
    # token = re.search(r"\{.token.:'(.*?)'", r.content.decode())[1]
    # upload_session = omnitools.randstr(32)
    # numfiles = len(urls)
    # gallery = ""
    # album = ""
    # for url in urls:
    #     r = s.post(postimages_domain + "/json/rr", headers={
    #         "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    #         "x-requested-with": "XMLHttpRequest"
    #     }, data={
    #         "token": token,
    #         "upload_session": upload_session,
    #         "url": url,
    #         "numfiles": numfiles,
    #         "gallery": gallery,
    #         "ui": json.dumps([24, 1920, 1080, "true", "", "", timestamp]),
    #         "optsize": "0",
    #         "expire": "0",
    #         "session_upload": session_upload
    #     })
    #     if r.status_code != 200:
    #         raise Exception("upload failed", r.status_code, r.content.decode())
    #     if numfiles > 1 and not gallery:
    #         gallery = r.json()["gallery"]
    #     if not album:
    #         album = r.json()["url"]
    # # print(album)
    # imges = get_album(s.get(album))
    # # print(imges)
    # pics = ThreadPool(10).imap_unordered(donw, imges)
    #
    # def get_num(x):
    #     try:
    #         return int(x.split("/")[-1].split(".")[0])
    #     except ValueError:
    #         return x
    #
    # imgs = sorted(pics, key=get_num)
    # return imgs
