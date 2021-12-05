import re
import requests
from addict import Dict
from ..mongo_connect import *
from ..PostImage import upload
from ..random_key import rankey
from imgurpython import ImgurClient
from ..screenshot import upload_img
from pyrogram.types import InlineKeyboardButton
from ..magic_funcs import IterSites, SauceLinks

# Vars
u = Mongo(URI, "SauceBOT", "users")
URL = "https://saucenao.com/search.php"
IMGUR_ID = config("IMGUR_ID", default=None)
IMGUR_SECRET = config("IMGUR_SECRET", default=None)
order = lambda some_list, x: [some_list[i:i + x] for i in range(0, len(some_list), x)]


# def __tt__(some_list, x):
#     btns = []
#     for i in range(0, len(some_list), x):
#         btns.append(some_list[i:i + x])
#     return btns


def toimgur(img):
    client = ImgurClient(client_id=IMGUR_ID, client_secret=IMGUR_SECRET)
    return client.upload_from_path(img)["link"]


class SauceNAO:
    @staticmethod
    def SauceNao(obj):
        return Dict(obj)

    @staticmethod
    def sauce(image, url=None, user_id=None):
        SauceNAO_API = config("SauceNAO_API", default=None)
        if user_id:
            c = confirm_ofdb(u, {"user_id": user_id})
            if c:
                SauceNAO_API = c[0]["SAUCE_API"]
            else:
                SauceNAO_API = None
        if url:
            image = upload([image])
        else:
            # files = {'file': open(image, 'rb')}
            sim = upload_img(file=image, name=rankey(6), expiration=900)
            image = sim.url
            # image = toimgur(image)
            # image = upload(image)
        if isinstance(image, str):
            pass
        elif isinstance(image, list):
            image = image[0]
        data = {"db": 999,
                "dbmaski": 3276,
                "url": image,
                "api_key": SauceNAO_API,
                "output_type": 2}
        # if url:
        r = requests.post(URL, params=data)
        print(r.json())
        # else:
        #     r = requests.post(URL, params=data, files=files)
        reg = SauceNAO.SauceNao(r.json())
        results = reg.results
        if reg.header.status == -1:
            inf = {"error": "**The anonymous account type does not permit API usage.**\n"
                            "Add your [API](https://saucenao.com/user.php?page=search-api)"
                            " with /api {and your api}\n"
                            "In the bot's private chat!"}
            return inf, inf, image, r.url
        if reg.header.status == -2:
            inf = {"error": "**Daily Search Limit Exceeded.**\n"
                            "Yor IP has exceeded the basic account type's daily limit of 200 searches."}
            return inf, inf, image, r.url
        else:
            if results:
                first = results[0]
                return first.header, first.data, image, r.url

    # return namedtuple("SauceNAObject", "header results")(*obj.values())


sauce = SauceNAO.sauce


def nao(lnk, url=None, user_id=None):
    snao = sauce(lnk, url=url, user_id=user_id)
    header, response, image_url, urlnao = snao
    # rd_ = re.search(r"&output_type.*", urlnao)
    # urlnao_clean = urlnao.replace(rd_[0], "")
    # res = re.search(r"&api_key.*", urlnao_clean)
    # try:
    #     url_safe = urlnao_clean.replace(res[0], "")
    # except TypeError:
    #     url_safe = urlnao_clean
    saucelinks = SauceLinks(image_url)
    yandex = saucelinks[0]
    google = saucelinks[1]
    url_safe = saucelinks[6]
    urlink, urlinks = None, None
    text = ""
    try:
        similarity = int(float(header.similarity))
    except AttributeError:
        similarity = 0
    if header["error"]:
        text += header["error"]
    else:
        source = response.source
        print(header)
        print(response)
    try:
        ext_urls = response.ext_urls
    except AttributeError:
        ext_urls = []
    if ext_urls or url_safe:
        ext_urls = ext_urls or []
        print(ext_urls)
        ext_urls.extend(saucelinks)
        try:
            if "i.pximg.net" in response.source or "twitter.com" in response.source:
                ext_urls.append(response.source)
        except AttributeError:
            pass
        unorder = [IterSites(i) for i in ext_urls]
        orl = lambda x: x
        # print(unorder)
        urlinks = sorted(unorder, key=orl)
        # print(urlinks)
    if urlinks:
        btns = []
        for i in urlinks:
            tx, ur = i
            btns.extend(
                [
                    InlineKeyboardButton(tx, url=ur)
                ]
            )
        try:
            lls = order(btns, 3)
        except ValueError:
            lls = btns
        urlink = lls
    else:
        if response.eng_name:
            c = "**Title:**\n"
            text += c + response.eng_name + "\n"
        elif response.jp_name:
            c = "**Japanese Title:**\n"
            text += c + response.jp_name + "\n"
    if similarity > 45:
        if response.title:
            c = "**Title:**\n"
            text += c + response.title + "\n"
        if response.creator or response.member_name:
            creator = response.creator
            if creator is None or isinstance(creator, dict):
                creator = response.member_name
            if isinstance(creator, list):
                c = "**Creator(s):**\n"
                creator = " ".join(creator)
            else:
                c = "**Creator:**\n"
            text += c + creator + "\n"
        if response.characters:
            characters = response.characters
            if isinstance(characters, list):
                c = "**Character(s):**\n"
                characters = ", ".join(characters)
            else:
                c = "**Character:**\n"
            text += c + characters + "\n"
        if response.source:
            if "i.pximg.net" in source:
                pass
            else:
                c = "**Source:**\n"
                text += c + source + "\n"
        if header.similarity:
            c = "**Similarity:**\n"
            text += c + header.similarity + "%\n"
        # text += f"[ ]({header.thumbnail})"
    else:
        if similarity > 0:
            text += "**No hay coincidencias relevantes.**\n"
        else:
            pass
    # rch = random.choice([urlnao_clean, google])
    return text, urlink, (url_safe, google, yandex), similarity
