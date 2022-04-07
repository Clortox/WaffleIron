from flask import Blueprint,request,json
from flask_pymongo import ObjectId
from ..app import mongo
from flask import render_template
from app.controllers.HomeController import homecontroller
from app.controllers.DocumentController import documentcontroller
from app.helpers.Utility import sendResponse

front = Blueprint("front", __name__)

testCourses = ["20145: CS43203 - Systems Programming", 
               "12412: CS49999 - Capstone", 
               "12393: CS45203 - Computer Network Security"]
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

@front.route('/', methods=['GET'])
def home():
    return homecontroller.index()

@front.route('/instructor', methods=['GET', 'POST'])
def instructor():
    return render_template("instructor.html",
        defaultFields = defaultFields,
        fieldsLen = len(defaultFields),
        testCourses = testCourses,
        courseLen = len(testCourses)
    )

@front.route('/administrator', methods=['GET', 'POST'])
def administrator():
    return render_template("administrator.html",
        requiredFields = requiredFields,
        fieldsLen = len(requiredFields)
    )

@front.route('/scheduler', methods=['GET', 'POST'])
def scheduler():
<<<<<<< HEAD
    return render_template("scheduler.html"
    )

@front.route('/signin', methods=['GET', 'POST'])
def signin():
    return render_template("signin.html")
=======
    return render_template("scheduler.html")

@front.route('/document/docx/<CRN>', methods=['GET'])
def document(CRN):
    return documentcontroller.document(CRN)

@front.route('/document/excel/', methods=['POST'])
def excel():
    excelDict = documentcontroller.excel(request.files['excelFile'])
    return sendResponse(excelDict)
>>>>>>> 3045aa5246794e37ec5949d737d9284c0ab217a7
