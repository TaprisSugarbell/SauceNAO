import re

try:
    from .slk import short
except ImportError:
    from slk import short

sits = {"Danbooru": "danbooru",
        "Gelbooru": "gelbooru",
        "DeviantArt": "deviantart",
        "TraceMOE": "trace.moe",
        "IQDB": "iqdb.org",
        "Ascii2d": "ascii2d.net",
        "TinEye": "www.tineye.com",
        "Pixiv": ["i.pximg.net", "www.pixiv.net"],
        "Twitter": "twitter",
        "SauceNAO": "saucenao.com",
        "Yandex": "yandex.com",
        "Google": "www.google.com",
        "ArtStation": "www.artstation.com",
        "MangaDex": "mangadex",
        "Baka-Updates": "www.mangaupdates.com",
        "MyAnimeList": "myanimelist.net",
        "Furaffinity": "www.furaffinity.net",
        "FurryNetwork": "furrynetwork.com"}


def IterSites(link):
    for k, v in sits.items():
        if isinstance(v, list):
            for i in v:
                mt = re.match(r"https?://{}".format(i), link)
                if mt:
                    break
        else:
            mt = re.match(r"https?://{}".format(v), link)
        if mt:
            if k == "Pixiv":
                link = "https://www.pixiv.net/artworks/" + link.split("/")[-1].split("=")[-1]
            return k, short(link)
    return "Unknown", short(link)


def notNone(*args):
    for i in args:
        if i:
            try:
                photo = i.photo
                if photo:
                    file_id = photo.file_id
                    return photo
            except AttributeError:
                pass


def SauceLinks(image_url, append=None):
    lenks = ["https://yandex.com/images/search?rpt=imageview&url={}",
             "https://www.google.com/searchbyimage?image_url={}&safe=off",
             "https://trace.moe/?url={}",
             "https://iqdb.org/?url={}",
             "https://www.tineye.com/search/?url={}",
             "https://ascii2d.net/search/url/{}",
             "https://saucenao.com/search.php?db=999&dbmaski=3276&url={}"]
    if append:
        tt = [i.format(image_url) for i in lenks]
        tt.append(append)
        return tt
    else:
        return [i.format(image_url) for i in lenks]
