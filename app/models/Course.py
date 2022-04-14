from ..app import mongo
from flask import request,json
import pprint

class Course():
    def __init__(self):
        pass

    def setPath(self, cID):
        return mongo[str(cID)]

    # This will be called when a new file has been created
    def createFile(self, cID, CRN, cYear, cSem, data={}):
        cTable = self.setPath(cID)
        file = {
            "_id": CRN,
            "cFields": data,
            "cYear": cYear,
            "cSem": cSem
        }
        cTable.insert_one(file)

    # These next functions will be called to update a particular field on a file
    def update_cyear(self, course_ID, CRN, yr):
        cTable = self.setPath(course_ID)
        file = cTable.find_one({"_id": CRN})
        cTable.update_one(file, {"$set": {"cYear":yr}})


    def update_csem(self, course_ID, CRN, sem):
        cTable = self.setPath(course_ID)
        file = cTable.find_one({"_id": CRN})
        cTable.update_one(file, {"$set": {"cSem": sem}})


    # This function takes a dictionary and edits the stored class fields
    # Useful to make one function call to change multiple fields!
    def update_cFields(self, course_ID, CRN, fields):
        data = get_data(course_ID, CRN)

        # First, checks to see which fields must be removed.
        # This is done by seeing which of the stored keys is
        # not present in the dataset being saved / overwritten.
        for key in data.keys():
            if fields.get(key) is None:
                remove_cFields(course_ID, CRN, key)

        # Any other data is set in the cFields. The "$set" command works
        # properly when you take into account Nested Documents.
        # This means that adding new fields and updating new fields will work
        # exactly the same!
        for key in fields.keys():
            add_cFields(course_ID, CRN, key, fields.get(key))


    # When arbitrarily updating the data fields, we will need to actively call these functions in order to
    # ensure the fields we want added are added, those we want deleted are deleted, and those we want updated
    # are updated. NOTE: Adding and Updating will produce the same results!

    # Please note, pymongo is treating the stored class fields as a nested document. In order to interact with
    # it using pymongo, you need to reference the outer data set name, in this case 'cFields', followed by a
    # period, followed by the name of the field you wish to perform queries on, then you provide data if necessary.
    # I recommend checking out Nested Documents documentation from MongoDB. I will find a good link for the chat!
    def add_cFields(self, course_ID, CRN, field_key, field_data):
        cTable = self.setPath(course_ID)
        file = cTable.find_one({"_id": CRN})
        cTable.update_one(file, {"$set": {'cFields.' + field_key: field_data}})


    def remove_cFields(self, course_ID, CRN, field_name):
        cTable = self.setPath(course_ID)
        file = cTable.find_one({"_id": CRN})
        cTable.update_one(file, {"$unset": {"cFields." + field_name: ""}})


    # This next function finds and returns and entire data file from the course
    def get_file(self, course_ID, CRN):
        cTable = self.setPath(course_ID)
        file = cTable.find_one({"_id": CRN})
        return file


    # This next function will only get the class fields from a particular file.
    # Particularly useful for updating the class fields...
    def get_data(self, course_ID, CRN):
        cTable = self.setPath(course_ID)
        file = cTable.find_one({"_id": CRN})
        return file["cFields"]


course=Course()
