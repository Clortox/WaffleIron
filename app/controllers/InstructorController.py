from flask import request
from flask import render_template
from flask import send_file
import hashlib
import io
from app.helpers.Utility   import generateSyllabus,parseExcelFile,sendResponse,getYear,getSemester
from app.models.Course     import course
from app.models.Lookup     import lookup
from app.models.User       import user
from app.helpers.passwords import encode_password

class InstructorController():

    defaultFields = [
        "Course Times",
        "Contact Information",
        "Assistant Information",
        "Course Description",
        "Prerequisites",
        "Kent Core Fulfillments",
        "Learning Outcomes",
        "Grading Scale",
        "Attendance Policy",
        "Course Schedule"
    ]

    requiredFields = [
        "Kent Core Courses",
        "WIC Courses",
        "Diversity Courses",
        "ELR Courses",
        "Health and Safety",
        "Copyright and Intellectual Property Rights",
        "Registration Requirement",
        "Course Withdrawal Deadlines",
        "Student Accessibility Policy",
        "Student Cheating and Plagiarism",
        "Respectful Student Conduct",
        "Diversity",
        "Student Survey of Instruction (SSI)"
    ]

    testCourses = [
        "20145: CS43203 - Systems Programming", 
        "12412: CS49999 - Capstone", 
        "12393: CS45203 - Computer Network Security"
    ]

    def __init__(self):
        pass

    #called on GET operations to /instructor/
    def getInstructor(self, instructor_email, CRN):
        # Get CRNs this instructor is in
        instructorCrns = user.getUserCRNs(instructor_email)

        # check validity of CRN
        if CRN == None or CRN not in instructorCrns:
            CRN = instructorCrns[0]

        # Get data for the selected course
        # get course ID
        course_ID = lookup.getCourseID(CRN)

        # get course details
        coursedata = {}
        coursedata = course.get_data(
            course_ID=course_ID,
            CRN = CRN)

        # if the default fields are not in the course already, place them
        for defField in self.defaultFields:
            if defField not in coursedata:
                coursedata[defField] = ''

        # get names of other courses this instructor is in
        otherCourses = []
        for crn in instructorCrns:
            otherCourses.append({
                "name" : lookup.getCourseName(crn),
                "CRN"  : crn,
                })

        # Return it to the view
        return render_template("instructor.html",
                otherCourses = otherCourses,
                otherCourseLen = len(otherCourses),
                fields = coursedata,
                fieldsLen = len(coursedata))


instructorcontroller = InstructorController()
