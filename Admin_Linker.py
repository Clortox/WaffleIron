import WaffleUser as User
import Waffle_admin as UPolicy
import Waffle_recommend as RPolicy


# Get From the policy tables ---------------------------
def getPolicy(table, PID):
    if table == 'UnivPolicies':
        return UPolicy.get_policy(PID)
    elif table == 'ReccPolicies':
        return RPolicy.get_policy(PID)


# Add a new policy to a table --------------------------
def addPolicy(table, PID, PName, PData):
    if table == 'UnivPolicies':
        return UPolicy.addpolicy(PID, PName, PData)
    elif table == 'ReccPolicies':
        return RPolicy.addrecpolicy(PID, PName, PData)


# Update an existing policy name -----------------------
def updatePolicyName(table, PID, PName):
    if table == 'UnivPolicies':
        UPolicy.updatepolicyname(PID, PName)
    elif table == 'ReccPolicies':
        RPolicy.updaterecpolicyname(PID, PName)


# Update an existing policy data -----------------------
def updatePolicyData(table, PID, PData):
    if table == 'UnivPolicies':
        UPolicy.updatepolicydata(PID, PData)
    elif table == 'ReccPolicies':
        RPolicy.updaterecpolicydata(PID, PData)


# Single update call -----------------------------------
def updatePolicy(table, PID, PName, PData):
    if table == 'UnivPolicies':
        policy = UPolicy.get_policy(PID)
        if PName != policy['pName']:
            updatePolicyName(table, PID, PName)

        if PData != policy['policy_data']:
            updatePolicyData(table, PID, PData)
    elif table == 'ReccPolicies':
        policy = RPolicy.get_policy(PID)
        if PName != policy['pName']:
            updatePolicyName(table, PID, PName)

        if PData != policy['policy_data']:
            updatePolicyData(table, PID, PData)


# Delete an existing policy ----------------------------
def deletePolicy(table, PID):
    if table == 'UnivPolicies':
        UPolicy.deletepolicy(PID)
    elif table == 'ReccPolicies':
        RPolicy.deleterecpolicy(PID)


# Create a new User ------------------------------------
def createNewUser(ID, contactInfo, role="PROF"):
    hash = ID + "1547"
    User.createUser(ID, hash, contact= contactInfo, role=role)


# Delete an existing User ------------------------------
def deleteUser(ID):
    User.deleteUser(ID)

