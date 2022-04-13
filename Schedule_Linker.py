import WaffleUser as User
import Waffle_Lookup as Look
import wafflecourse as Course


def import_call(fileDict):
    # This will fill the lookup table, modify the CRNs of professors,
    # and will fill basic file information using the file imported from the excel doc
    profs = User.getAllProfs()

    # Clears all CRN values from the profs --> only current CRNs will be editable
    for prof in profs:
        for CRN in prof['CRN']:
            User.removeCRN(prof["_id"], CRN)

    # Begins looping through the Entries in the excel file dictionary and makes the
    # following changes in the system:
    """
    LOOKUP_TABLE
        a) Will add a new course to the lookup table if it does not yet exist
        b) Will add CRNs to corresponding courses in the lookup table
    
    USER_TABLE
        a) Will add CRNs to all corresponding professors
        b) Will create a Professor account if not found
    
    COURSE_TABLES
        a) Will create base files for the CRN values using information pulled from the
            excel doc
    """
    for CRN in fileDict:
        # First, edit the lookup table.
        if Look.getCourseName_cID(CRN['courseNumber']) == 'ER404':
            Look.addCourse(CRN['courseNumber'], CRN['title'], [CRN['CRN']])
        else:
            Look.addCourseCRN(CRN['courseNumber'], CRN['CRN'])

        # Now, adds the CRN to the corresponding prof
        prof = findProf(profs, CRN['instructorEmail'])
        if prof == 'ER404':
            # Will create a new professor if it is not found in the prof list
            pID = CRN['instructorEmail'].split('@')

            # ---------------------------------------------------------------------------------------------------
            # ------ REPLACE THE HASH VALUE WITH A AUTO GENERATED TEMPORARY!!!! Second parameter! ---------------
            # ---------------------------------------------------------------------------------------------------

            User.createUser(pID[0], pID[0], contact={'email': CRN['instructorEmail']}, crn=[CRN['CRN']])
        else:
            # noinspection PyTypeChecker
            User.addCRN(prof['_id'], CRN['CRN'])

        # Finally, creates the class files with the basic information gathered by the excel doc
        data = {'title': CRN['title'],
                'section': CRN['section']}

        if CRN['multipleMeetingPlaces']:
            data['lectureBuilding'] = CRN['building'][0]
            data['lectureRoom'] = CRN['room'][0]
            data['labBuilding'] = CRN['building'][1]
            data['labRoom'] = CRN['room'][1]
        else:
            data['lectureBuilding'] = CRN['building']
            data['labRoom'] = CRN['room']

        if CRN['multipleMeetingTimes']:
            data['lectureTime'] = CRN['time'][0]
            data['labTime'] = CRN['time'][1]
        else:
            data['lectureTime'] = CRN['time']

        if CRN['multipleMeetingDays']:
            data['lectureDays'] = CRN['meetingDays'][0]
            data['labDays'] = CRN['meetingDays'][1]
        else:
            data['lectureDays'] = CRN['meetingDays']

        Course.createFile(CRN['courseNumber'], CRN['CRN'], '', '', data)


# Finds a prof using their email
def findProf(profs, profEmail):
    for prof in profs:
        if prof['contactInfo']['email'] == profEmail:
            return prof
    return "ER404"


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
    WIll make a testing script for this later.
    :return:
    """

    return


if __name__ == "__main__":
    main()