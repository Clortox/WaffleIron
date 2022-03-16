from ..app import mongo
from flask import request,json
from flask_pymongo import ObjectId
#password hashing
import hashlib
from enum import Enum

class Role(Enum):
    ADMIN = 1
    PROFESSOR = 2

class User():
    def __init__(self):
        pass

    #get some user by id (TODO)
    def getUser(_id):
        return

    def getAllUsers(_id):
        return

    def registerUser(self, _user_flashlineID, user_pw):
        return

user=User()
