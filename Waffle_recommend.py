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
    # deletepolicy('123')

    for i in range(3):
        addrecpolicy(i,policyname[i],"The test recommend policy")
        print(get_policy(i))
    
    updaterecpolicyname('123',"Ishva policy")
    print(get_policy('123'))
    updaterecpolicydata('123',"This is Ishva policy")
    print(get_policy('123'))

   # deletepolicy('123')


if __name__ == "__main__":
    main()