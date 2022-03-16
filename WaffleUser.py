from pymongo import MongoClient
import pprint


def setPath():
    return MongoClient()['WaffleIron_DB']['users']


def createUser(ID, pWord, contact, crn=[], role="PROF"):
    users = setPath()
    userPost = {
        "_id": ID,
        "pass": pWord,
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
