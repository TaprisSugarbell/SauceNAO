import os
from decouple import config
try:
    from .mongo_db import *
except ImportError:
    from mongo_db import *


# Variables
URI = config("MONGO_URL", default=None)


async def confirm(user_db, data=None):
    if data is None:
        data = {}
    return user_db.find(data)


async def add_(user_db, data=None):
    if data is None:
        data = {}
    return user_db.insert_one(data)


async def update_(user_db, old_data=None, new_data=None):
    if old_data is None:
        old_data = {}
    if new_data is None:
        new_data = {}
    return user_db.update_one(old_data, new_data)


async def remove_(user_db, data=None):
    if data is None:
        data = {}
    return user_db.delete_one(data)


def confirm_ofdb(user_db, data=None):
    if data is None:
        data = {}
    return user_db.find(data)


def add_ofdb(user_db, data=None):
    print(data)
    if data is None:
        data = {}
    return user_db.insert_one(data)


def update_ofdb(user_db, old_data=None, new_data=None):
    if old_data is None:
        old_data = {}
    if new_data is None:
        new_data = {}
    return user_db.update_one(old_data, new_data)


def remove_ofdb(user_db, data=None):
    if data is None:
        data = {}
    return user_db.delete_one(data)


def remove_many(user_db, data=None):
    if data is None:
        data = {}
    return user_db.delete_many(data)
