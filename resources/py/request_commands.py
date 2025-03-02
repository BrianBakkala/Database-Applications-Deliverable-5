from resources.py.db_helper import DBHelper
from resources.py import util
import json

db = DBHelper(host="localhost", user="root", password="", database="cs727_baseball")


def create(obj):
    return db.create(table=obj["table"], data=obj["data"])


def delete(obj):
    return db.delete(table=obj["table"], record_id=obj["record_id"])


def update(obj):
    return db.update(table=obj["table"], record_id=obj["record_id"], data=obj["data"])
