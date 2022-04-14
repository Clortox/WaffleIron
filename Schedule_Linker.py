import WaffleUser as User
import Waffle_Lookup as Look


# This function is used to call all data stored in the lookup table
def getLookup():
    return Look.getCourses()


# This function will get the prof information relevant to the scheduler:
# The professor ID, name, and their CRN values
def getProfInfo():
    retProfs = {}
    profs = User.getAllProfs()
    for prof in profs:
        retProfs[prof['_id']] = {'name': prof['contactInfo']['name'],
                                 'CRN': prof['CRN']}
    return retProfs


# Remove a CRN from a prof
def removeCRN(pID, CRN):
    User.removeCRN(pID, CRN)


# Add a CRN to a prof
def addCRN(pID, CRN):
    User.addCRN(pID, CRN)


# Add a CRN to a course
def addCRNCourse(cID, CRN):
    Look.addCourseCRN(cID, CRN)


# Remove a CRN from a course
def removeCRNCourse(cID, CRN):
    Look.removeCourseCRN(cID, CRN)


# Add a Course
def addCourse(cID, cName, crn=[]):
    Look.addCourse(cID, cName, crn)


# Remove a course
def removeCourse(cID):
    Look.DeleteCourse(cID)


# Edit a course name
def editCourseName(cID, name):
    Look.editCourseName(cID, name)


def main():
    """
    :return:
    """

    return


if __name__ == "__main__":
    main()