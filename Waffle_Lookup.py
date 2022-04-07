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


def DeleteCourse(ID):
    WaffleCourse = setPath()
    WaffleFiles = MongoClient()['WaffleIron_DB'][ID]

    # Deletes all files from a course when removing a course
    for file in WaffleFiles.find({}):
        WaffleFiles.delete_one(file)


    WaffleCourse.delete_one(course)
    print("Course " + ID + " has been deleted.")


def main():
    # Uncomment these if an issue occurs and the files were not deleted!
    # DeleteCourse('WC44543')
    # DeleteCourse('WI44342')
    # DeleteCourse('WE00340')

    addCourse('WC44543', 'Waffle Cooking', [40302, 45002, 50000])
    addCourse('WI44342', 'Waffle Iron Training')
    addCourse('WE00340', 'Waffle Eating Training', [50123, 623443, 10489])

    name = getCourseName(50129)
    print(name)

    DeleteCourse('WC44543')
    DeleteCourse('WI44342')
    DeleteCourse('WE00340')

    testDict = {"Data": "Value", "Value": "Another Value", "Final": "F"}
    for key in testDict.keys():
        print(key)
    print(testDict.get("Data"))
    print(testDict.get("OtherData"))


if __name__ == '__main__':
    main()
