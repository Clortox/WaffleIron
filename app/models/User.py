from ..app import mongo
from flask import request,json, Flask, session
#password hashing
import hashlib
from enum import Enum

# Session ID
import uuid

class Role(Enum):
    ADMIN = 1
    PROFESSOR = 2
    SCHEDULER = 3

class User():
    def __init__(self):
        pass

    def setPath(self):
        return mongo['users']

    def startSession(self, email):
        session['logged_in'] = True
        session['user_email'] = email
        return session

    def confirmLogin(self, ID, hash):
        users = self.setPath()
        try:
            profile = users.find_one({"_id": ID})
            if profile["hash"] == hash:
                return True
            else:
                return False
        except TypeError:
            return False


    def createUser(self, ID, hash, contact={}, crn=[], role="PROF"):
        users = self.setPath()
        userPost = {
            "_id": ID,
            "hash": hash,
            "contactInfo": contact,
            "role": role,
            "CRN": crn
        }
        users.insert_one(userPost)


    def updateContact(self, ID, contact):
        users = self.setPath()
        user = users.find_one({"_id": ID})
        users.update_one(user, {"$set": {"contactInfo": contact}})

    def deleteUser(self, ID):
        users = self.setPath()
        user = users.find_one({"_id": ID})
        users.delete_one(user)
        print("User: " + ID + " has been deleted.")
        # return True


    def setRole(self, ID, role):
        users = self.setPath()
        user = users.find_one({"_id": ID})
        users.update_one(user, {"$set": {"role": role}})


    # This is a temporary placement just to access and change the password.
    # This will be moved when more security and login stuff is added.
    def changePass(self, ID, hash):
        users = self.setPath()
        user = users.find_one({"_id": ID})
        users.update_one(user, {"$set": {"hash": hash}})
        


    def addCRN(self, ID, crn):
        users = self.setPath()
        user = users.find_one({"_id": ID})
        print(type(user))
        users.update_one(user, {"$push": {"CRN": crn}})


    def removeCRN(self, ID, crn):
        users = self.setPath()
        user = users.find_one({"_id": ID})
        users.update_one(user, {"$pull": {"CRN": crn}})


    # Getter methods for the user class
    def getUserCRNs(self, ID):
        users = self.setPath()
        return users.find_one({'_id': ID})['CRN']


    def getUserContact(self, ID):
        users = self.setPath()
        return users.find_one({'_id': ID})['contactInfo']


    def getUserRole(self, ID):
        users = self.setPath()
        return users.find_one({"_id": ID})["role"]

    def getUserHash(self, ID):
        users = self.setPath()
        profile = users.find_one({"_id": ID})
        return profile["hash"]


    def confirmUserCRN(self, ID, CRN):
        CRNList = self.getUserCRNs(ID)
        if CRNList.count(CRN) > 0:
            return True
        else:
            return False

    def userExists(self, ID):
        users = self.setPath()
        if users.find_one({'_id': ID}) == None:
            return False
        else:
            return True


    # Function used by the Schedule_Linker to get all of the users from the system
    def getAllProfs(self):
        profs = {}
        users = self.setPath()
        for user in users.find({}):
            if user["role"] == 'PROF':
                profs[user['_id']] = user
        return profs


user=User()
