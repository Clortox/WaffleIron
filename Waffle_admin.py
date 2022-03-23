from pymongo import MongoClient


def setPath():
    return MongoClient()['WaffleIron_DB']['reqpolicies']

def addpolicy(pID, policyname, pdata):
    WafflePolicy = setPath()
    adminPost = {
        "_id": pID,
        "pName": policyname,
        "policy_data": pdata
    }

    WafflePolicy.insert_one(adminPost)

def deletepolicy(pId):
    WafflePolicy = setPath()
    policy = WafflePolicy.find_one({'_id': pId})
    WafflePolicy.delete_one(policy)
    print("policy " + ID + " has been deleted.")

def updatepolicyname(pId,policyname):
    WafflePolicy = setPath()
    policy = WafflePolicy.find_one({'_id': pId})
    WafflePolicy.update_one(policy, {"$set": {"pName":policyname}})

def updatepolicydata(pId,data):
    WafflePolicy = setPath()
    policy = WafflePolicy.find_one({'_id': pId})
    WafflePolicy.update_one(policy, {"$set": {"policy_data":data}})

def get_policy(pId):
    WafflePolicy = setPath()
    policy = WafflePolicy.find_one({"_id": pId})
    return policy


def main():
    addpolicy('123',"university","This is university policy")
    print(get_policy('123'))
    updatepolicyname('123',"Ishva policy")
    print(get_policy('123'))
    updatepolicydata('123',"This is Ishva policy")
    print(get_policy('123'))


if __name__ == "__main__":
    main()