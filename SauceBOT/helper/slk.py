import base64
import requests
import pyshorteners


def short(link):
    s = pyshorteners.Shortener()
    return s.tinyurl.short(link)


def cacalinks(link):
    ln = base64.b64encode(link.encode())
    r = requests.post("https://cacalinks.com/api.php", data={"url": ln})
    return r.json()["msg"]
