from ..app import mongo
from flask import request,json
import pprint

class RecomnededPolicy():
    def __init__(self):
        pass

    policyname = ["universitypolicy","grading","sas"]

    def setPath(self):
        return mongo['recpolicies']


    def addrecpolicy(self, pID, pdata):
        WafflePolicy = self.setPath()
        adminPost = {
            "_id": pID,
            #"pName": policyname,
            "policy_data": pdata
        }

        WafflePolicy.insert_one(adminPost)

    def deleterecpolicy(self, pId):
        WafflePolicy = self.setPath()
        policy = WafflePolicy.find_one({'_id': pId})
        WafflePolicy.delete_one(policy)
        print("policy " + pId + " has been deleted.")

    def updaterecpolicydata(self, pId,data):
        WafflePolicy = self.setPath()
        policy = WafflePolicy.find_one({'_id': pId})
        WafflePolicy.update_one(policy, {"$set": {"policy_data":data}})

    def get_policy(self, pId):
        WafflePolicy = self.setPath()
        policy = WafflePolicy.find_one({"_id": pId})
        return policy

    def getAllPolicy(self):
        WafflePolicy = self.setPath()
        policy = WafflePolicy.find()
        return policy

recomendedpolicy=RecomnededPolicy()
