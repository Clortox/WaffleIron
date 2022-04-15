from ..app import mongo
from flask import request,json
import pprint

class Lookup():
    def __init__(self):
        pass

    def setPath(self):
        return mongo['Waffle_Lookup']


    def addCourse(self, ID, name, crn=[]):
        WaffleCourse = self.setPath()
        coursePost = {
            "_id": ID,
            "cName": name,
            "CRNs": crn
        }

        WaffleCourse.insert_one(coursePost)


    def getCourseName(self, crn):
        WaffleCourse = self.setPath()

        for c in WaffleCourse.find():
            if c['CRNs'].count(crn) > 0:
                return c['cName']
        return 'ER404'


    def getCourseName_cID(self, cID):
        WaffleCourse = self.setPath()

        try:
            course = WaffleCourse.find_one({"_id": cID})
            return course['cName']
        except TypeError:
            return 'ER404'



    def getCourseID(self, crn):
        WaffleCourse = self.setPath()

        for c in WaffleCourse.find():
            if c['CRNs'].count(crn) > 0:
                return c['_id']
        return 'ER404'

    def getCourseCRNs(self, cID):
        WaffleCourse = self.setPath()
        try:
            return WaffleCourse.find_one({"_id": cID})['CRNs']
        except TypeError:
            return "Course Information Not Found."


    def addCourseCRN(self, cID, CRN):
        WaffleCourse = self.setPath()
        course = WaffleCourse.find_one({"_id": cID})
        WaffleCourse.update_one(course, {"$push": {"CRNs": CRN}})


    def removeCourseCRN(self, cID, CRN):
        WaffleCourse = self.setPath()
        course = WaffleCourse.find_one({"_id": cID})
        WaffleCourse.update_one(course, {"$pull": {"CRNs": CRN}})


    def DeleteCourse(self, ID):
        WaffleCourse = self.setPath()
        WaffleFiles = MongoClient()['WaffleIron_DB'][ID]

        # Deletes all files from a course when removing a course
        for file in WaffleFiles.find({}):
            WaffleFiles.delete_one(file)


        WaffleCourse.delete_one(course)
        print("Course " + ID + " has been deleted.")


    def editCourseName(self, ID, name):
        WaffleCourse = self.setPath()
        course = WaffleCourse.find_one({"_id": ID})
        WaffleCourse.update_one(course, {"$set": {"cName": name}})


    def getCourses(self):
        WaffleCourse = self.setPath()
        return WaffleCourse.find({})

lookup=Lookup()
