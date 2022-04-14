from flask import Blueprint,request,json
from ..app import mongo
#from app.waffleauth import fbsignin
from flask import render_template
from flask import request, redirect, make_response
from app.controllers.HomeController import homecontroller
from app.controllers.DocumentController import documentcontroller
from app.helpers.Utility import sendResponse

from Schedule_Linker import getLookup
from random import seed, randint
import passwords


front = Blueprint("front", __name__)

testCourses = ["20145: CS43203 - Systems Programming", 
               "12412: CS49999 - Capstone", 
               "12393: CS45203 - Computer Network Security"
]

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

@front.route('/saveSuccess', methods=['POST'])
def sendInfo():
    descriptions = request.form

    for key in descriptions.keys():
        for value in descriptions.getlist(key):
            print(key,":",value)

    return render_template("saveSuccess.html")


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
    return render_template("scheduler.html")


# Displays register page
@front.route('/register')
def register_page():
    return render_template("register.html")


# Handles register operations
@front.route('/register', methods=['POST'])
def register():
    email = request.form['email']
    password = request.form['password']
    passwordConfirm = request.form['password_confirm']

    if password != passwordConfirm:
        return render_template('register.html')

    password = passwords.encode_password(password)

    print("Email: ", email)
    print("password: ", password)

    return redirect("/login")


@front.route('/login')
def login_page():
    return render_template("login.html")


@front.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

    resp = make_response(render_template("login.html"))
    resp.set_cookie('userID', email)

    return resp


@front.route('/document/docx/<CRN>', methods=['GET'])
def document(CRN):
    return documentcontroller.document(CRN)


@front.route('/document/excel/', methods=['POST'])
def excel():
    excelDict = documentcontroller.excel(request.files['excelFile'])
    return sendResponse(excelDict)
