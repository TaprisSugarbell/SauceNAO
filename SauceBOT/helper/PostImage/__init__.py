try:
    from .upload import upload
except ImportError:
    from upload import upload
import random
import string
import cloudinary
from decouple import config
from cloudinary import uploader

CLOUD_NAME = config("CLOUD_NAME")
CLOUD_API = config("CLOUD_KEY")
CLOUD_SECRET = config("CLOUD_SECRET")

cloudinary.config(
  cloud_name=CLOUD_NAME,
  api_key=CLOUD_API,
  api_secret=CLOUD_SECRET
)


def upload_f(file, public_id="".join(random.choice(string.hexdigits) for _ in range(10))):
    fd = upload(cloudinary.uploader.upload(file, public_id=public_id)["url"])
    cloudinary.uploader.destroy(public_id)
    return fd[0]

