import WaffleUser as User
import Waffle_Lookup as Look
import wafflecourse as Course


def find_file(uID, CRN):
    # Finds a file if it is owned by the User
    if User.confirmUserCRN(uID, CRN):
        cID = Look.getCourseID(CRN)
        try:
            file = Course.get_file(cID, CRN)
        # Creates a new file if a TypeError is raised (File does not exist)
        except TypeError:
            file = Course.createFile(cID, CRN, "", "")
        return file
    # Finds a file if it is 'related' to the prof's file
    elif isCRNRelated(uID, CRN):
        cID = Look.getCourseID(CRN)
        try:
            file = Course.get_file(cID, CRN)
            return file
        except TypeError:
            return "File is not accessible or does not exist"
    # Responds that the file is not accessible or doesn't exist
    else:
        return "File is not accessible or does not exist"


# Determines if a CRN value belongs to the same
# course as one of the user's CRN values
def isCRNRelated(uID, CRN):
    uCRNs = User.getUserCRNs(uID)
    cID = Look.getCourseID(CRN)
    cCRNs = Look.getCourseCRNs(cID)
    for c in uCRNs:
        if cCRNs.count(c) > 0:
            return True
    return False


# Utilizes these three methods to return all required user
# info without accessing the user password
def getUserInfo(uID):
    contact = User.getUserContact(uID)
    role = User.getUserRole(uID)
    CRNs = User.getUserCRNs(uID)
    return contact, role, CRNs


# Finds all class names for the given CRNs a professor has.
def getClassNames(uID):
    CRN_list = User.getUserCRNs(uID)
    classNames = []
    for CRN in CRN_list:
        classNames.append(Look.getCourseName(CRN))
    return classNames


def main():
    # User.deleteUser('nProf56')
    # Look.DeleteCourse('WE54000')
    # Look.DeleteCourse('WC49999')
    # Look.DeleteCourse('WB32500')

    User.createUser('nProf56', "Coconut", ["New Professor", "nProf56@Waffles.inc", 4543223000], [54000, 49999, 32500])
    Look.addCourse('WE54000', "Waffle Eating Core", [54000, 55000, 56000])
    Look.addCourse('WC49999', "Waffle Cooking Concepts", [49999, 48999, 47999])
    Look.addCourse('WB32500', "Waffle Fundamentals", [32500, 25000])

    print(User.confirmLogin('nProf56', 'Coconut'))
    getClassNames('nProf56')
    print(getClassNames('nProf56'))

    print(getUserInfo('nProf56'))
    print(User.confirmUserCRN('nProf56', 54000))
    print(User.confirmUserCRN('nProf56', 54001))

    User.deleteUser('nProf56')
    Look.DeleteCourse('WE54000')
    Look.DeleteCourse('WC49999')
    Look.DeleteCourse('WB32500')


if __name__ == "__main__":
    main()
