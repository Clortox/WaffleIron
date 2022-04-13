from pymongo import MongoClient
import pprint


def setPath():
    return MongoClient()['WaffleIron_DB']['users']


def confirmLogin(ID, hash):
    users = setPath()
    try:
        profile = users.find_one({"_id": ID})
        if profile["hash"] == hash:
            return True
        else:
            return False
    except TypeError:
        return False


def createUser(ID, hash, contact={}, crn=[], role="PROF"):
    users = setPath()
    userPost = {
        "_id": ID,
        "hash": hash,
        "contactInfo": contact,
        "role": role,
        "CRN": crn
    }
    users.insert_one(userPost)


def updateContact(ID, contact):
    users = setPath()
    user = users.find_one({"_id": ID})
    users.update_one(user, {"$set": {"contactInfo": contact}})


def deleteUser(ID):
    users = setPath()
    user = users.find_one({"_id": ID})
    users.delete_one(user)
    print("User: " + ID + " has been deleted.")
    # return True


def setRole(ID, role):
    users = setPath()
    user = users.find_one({"_id": ID})
    users.update_one(user, {"$set": {"role": role}})


# This is a temporary placement just to access and change the password.
# This will be moved when more security and login stuff is added.
def changePass():
    return


def addCRN(ID, crn):
    users = setPath()
    user = users.find_one({"_id": ID})
    users.update_one(user, {"$push": {"CRN": crn}})


def removeCRN(ID, crn):
    users = setPath()
    user = users.find_one({"_id": ID})
    users.update_one(user, {"$pull": {"CRN": crn}})


# Getter methods for the user class
def getUserCRNs(ID):
    users = setPath()
    return users.find_one({'_id': ID})['CRN']


def getUserContact(ID):
    users = setPath()
    return users.find_one({'_id': ID})['contactInfo']


def getUserRole(ID):
    users = setPath()
    return users.find_one({"_id": ID})["role"]


def confirmUserCRN(ID, CRN):
    CRNList = getUserCRNs(ID)
    if CRNList.count(CRN) > 0:
        return True
    else:
        return False


# Function used by the Schedule_Linker to get all of the users from the system
def getAllProfs():
    profs = {}
    users = setPath()
    for user in users.find({}):
        if user["role"] == 'PROF':
            profs[user['_id']] = user
    return profs


def main():
    users = setPath()
    if users.find_one({"_id": "BrianID"}):
        deleteUser("BrianID")

    createUser("BrianID", "BrianPass", ["Brian", "Brian@Waffles.org", 3303232210], [40000, 50000], "ADMIN")
    user = users.find_one({"_id": "BrianID"})
    uID = user["_id"]

    pprint.pprint(user)
    print("\n\n")

    print("Update Contact:")
    updateContact(uID, ["Brian Lastname", "Last@kent.edu", 4405567342])
    user = users.find_one({"_id": "BrianID"})
    pprint.pprint(user)
    print("\n\n")

    print("Remove Contact Info:")
    updateContact(uID, ["Brian Behnke", 1234567890])
    user = users.find_one({"_id": "BrianID"})
    pprint.pprint(user)
    print("\n\n")

    print("Set Role:")
    setRole(uID, "PROF")
    user = users.find_one({"_id": "BrianID"})
    pprint.pprint(user)
    print("\n\n")

    print("Add CRN:")
    addCRN(uID, 32123)
    user = users.find_one({"_id": "BrianID"})
    pprint.pprint(user)
    print("\n\n")

    print("Remove CRN:")
    removeCRN(uID, 50000)
    user = users.find_one({"_id": "BrianID"})
    pprint.pprint(user)
    print("\n\n")

    deleteUser(uID)


if __name__ == "__main__":
    main()
