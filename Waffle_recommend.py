from pymongo import MongoClient


def setPath():
    return MongoClient()['WaffleIron_DB']['recpolicies']

policyname = ["universitypolicy","grading","sas"]

def addrecpolicy(pID, policyname, pdata):
    WafflePolicy = setPath()
    adminPost = {
        "_id": pID,
        "pName": policyname,
        "policy_data": pdata
    }

    WafflePolicy.insert_one(adminPost)

def deleterecpolicy(pId):
    WafflePolicy = setPath()
    policy = WafflePolicy.find_one({'_id': pId})
    WafflePolicy.delete_one(policy)
    print("policy " + pId + " has been deleted.")

def updaterecpolicyname(pId,policyname):
    WafflePolicy = setPath()
    policy = WafflePolicy.find_one({'_id': pId})
    WafflePolicy.update_one(policy, {"$set": {"pName":policyname}})

def updaterecpolicydata(pId,data):
    WafflePolicy = setPath()
    policy = WafflePolicy.find_one({'_id': pId})
    WafflePolicy.update_one(policy, {"$set": {"policy_data":data}})

def get_policy(pId):
    WafflePolicy = setPath()
    policy = WafflePolicy.find_one({"_id": pId})
    return policy


def main():
    # Uncomment this next line if an issue occurs and you need to clear the db of the test data!
    # deleterecpolicy('0')
    # deleterecpolicy('1')
    # deleterecpolicy('2')

    for i in range(3):
        addrecpolicy(i,policyname[i],"The test recommend policy")
        print(get_policy(i))
    
    updaterecpolicyname('1',"Ishva policy")
    print(get_policy('1'))
    updaterecpolicydata('2',"This is Ishva policy")
    print(get_policy('2'))

    deleterecpolicy('0')
    deleterecpolicy('1')
    deleterecpolicy('2')


if __name__ == "__main__":
    main()
