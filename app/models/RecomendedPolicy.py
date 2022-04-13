from ..app import mongo
from flask import request,json
import pprint

class RecomnededPolicy():
    def __init__(self):
        pass

    policyname = ["universitypolicy","grading","sas"]

    def setPath(self):
        return MongoClient()['recpolicies']


    def addrecpolicy(self, pID, policyname, pdata):
        WafflePolicy = setPath()
        adminPost = {
            "_id": pID,
            "pName": policyname,
            "policy_data": pdata
        }

        WafflePolicy.insert_one(adminPost)

    def deleterecpolicy(self, pId):
        WafflePolicy = setPath()
        policy = WafflePolicy.find_one({'_id': pId})
        WafflePolicy.delete_one(policy)
        print("policy " + pId + " has been deleted.")

    def updaterecpolicyname(self, pId,policyname):
        WafflePolicy = setPath()
        policy = WafflePolicy.find_one({'_id': pId})
        WafflePolicy.update_one(policy, {"$set": {"pName":policyname}})

    def updaterecpolicydata(self, pId,data):
        WafflePolicy = setPath()
        policy = WafflePolicy.find_one({'_id': pId})
        WafflePolicy.update_one(policy, {"$set": {"policy_data":data}})

    def get_policy(self, pId):
        WafflePolicy = setPath()
        policy = WafflePolicy.find_one({"_id": pId})
        return policy

recomendedpolicy=RecomnededPolicy()
