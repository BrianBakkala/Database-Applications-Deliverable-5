from resources.py.db_helper import DBHelper
from resources.py import util
import json

db = DBHelper(host="localhost", user="root", password="", database="cs727_baseball")


def create(obj):
    return db.create(obj["table"], obj["data"])
