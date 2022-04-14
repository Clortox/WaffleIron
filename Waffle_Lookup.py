from pymongo import MongoClient


def setPath():
    return MongoClient()['WaffleIron_DB']['Waffle_Lookup']


def addCourse(ID, name, crn=[]):
    WaffleCourse = setPath()
    coursePost = {
        "_id": ID,
        "cName": name,
        "CRNs": crn
    }

    WaffleCourse.insert_one(coursePost)


def getCourseName(crn):
    WaffleCourse = setPath()

    for c in WaffleCourse.find():
        if c['CRNs'].count(crn) > 0:
            return c['cName']
    return 'ER404'


def getCourseName_cID(cID):
    WaffleCourse = setPath()

    try:
        course = WaffleCourse.find_one({"_id": cID})
        return course['cName']
    except TypeError:
        return 'ER404'



def getCourseID(crn):
    WaffleCourse = setPath()

    for c in WaffleCourse.find():
        if c['CRNs'].count(crn) > 0:
            return c['_id']
    return 'ER404'

def getCourseCRNs(cID):
    WaffleCourse = setPath()
    try:
        return WaffleCourse.find_one({"_id": cID})['CRNs']
    except TypeError:
        return "Course Information Not Found."


def addCourseCRN(cID, CRN):
    WaffleCourse = setPath()
    course = WaffleCourse.find_one({"_id": cID})
    WaffleCourse.update_one(course, {"$push": {"CRNs": CRN}})


def removeCourseCRN(cID, CRN):
    WaffleCourse = setPath()
    course = WaffleCourse.find_one({"_id": cID})
    WaffleCourse.update_one(course, {"$pull": {"CRNs": CRN}})


def DeleteCourse(ID):
    WaffleCourse = setPath()
    WaffleFiles = MongoClient()['WaffleIron_DB'][ID]

    # Deletes all files from a course when removing a course
    for file in WaffleFiles.find({}):
        try:
            WaffleFiles.delete_one(file)
        except TypeError:
            break

    WaffleCourse.delete_one({"_id":ID})
    print("Course " + ID + " has been deleted.")


def editCourseName(ID, name):
    WaffleCourse = setPath()
    course = WaffleCourse.find_one({"_id": ID})
    WaffleCourse.update_one(course, {"$set": {"cName": name}})


def getCourses():
    WaffleCourse = setPath()
    cursor = WaffleCourse.find()
    courseDict = {}
    for c in cursor:
        courseDict[c['_id']] = c
    return courseDict


def main():
    #addCourse("6666", "Another New Course", ["1212", '5856'])
    #DeleteCourse('6666')
    #DeleteCourse('5555')
    print(getCourses())


if __name__ == '__main__':
    main()
