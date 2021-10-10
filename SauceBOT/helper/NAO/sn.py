import re
import requests
from addict import Dict
from decouple import config
from ..PostImage import upload
from ..random_key import rankey
from imgurpython import ImgurClient
from ..magic_funcs import IterSites
from ..screenshot import upload_img
from pyrogram.types import InlineKeyboardButton

# Vars
URL = "https://saucenao.com/search.php"
IMGUR_ID = config("IMGUR_ID", default=None)
IMGUR_SECRET = config("IMGUR_SECRET", default=None)
SauceNAO_API = config("SauceNAO_API", default=None)
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
    def sauce(image, url=None):
        files = None
        if url:
            image = upload([image])
        else:
            files = {'file': open(image, 'rb')}
            sim = upload_img(file=image, name=rankey(10), expiration=900)
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
        if url:
            r = requests.post(URL, params=data)
        else:
            r = requests.post(URL, params=data, files=files)
        results = SauceNAO.SauceNao(r.json()).results
        # print(results)
        if results:
            first = results[0]
            return first.header, first.data, image, r.url
    # return namedtuple("SauceNAObject", "header results")(*obj.values())


sauce = SauceNAO.sauce


def nao(lnk, url=None):
    snao = sauce(lnk, url=url)
    header, response, image_url, urlnao = snao
    similarity = int(float(header.similarity))
    rd_ = re.search(r"&output_type.*", urlnao)
    urlnao_clean = urlnao.replace(rd_[0], "")
    res = re.search(r"&api_key.*", urlnao)
    url_safe = urlnao.replace(res[0], "")
    source = response.source
    urlink, urlinks = None, None
    text = ""
    print(header)
    print(response)
    yandex = f"https://yandex.com/images/search?rpt=imageview&url={image_url}"
    google = f"https://www.google.com/searchbyimage?image_url={image_url}&safe=off"
    tracemoe = f"https://trace.moe/?url={image_url}"
    iqdb = f"https://iqdb.org/?url={image_url}"
    tineye = f"https://www.tineye.com/search/?url={image_url}"
    ascii2d = f"https://ascii2d.net/search/url/{image_url}"
    if response.ext_urls or url_safe:
        ext_urls = response.ext_urls or []
        print(ext_urls)
        ext_urls.extend([url_safe,
                         yandex,
                         google,
                         tracemoe,
                         iqdb,
                         tineye,
                         ascii2d])
        if "i.pximg.net" in response.source or "twitter.com" in response.source:
            ext_urls.append(response.source)
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
            text += c + header.similarity + "\n"
        # text += f"[ ]({header.thumbnail})"
    else:
        text += "**No hay coincidencias relevantes.**\n"
    # rch = random.choice([urlnao_clean, google])
    return text, urlink, urlnao_clean, google, similarity
