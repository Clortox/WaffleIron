from flask import Blueprint,request,json, flash
from ..app import mongo
from flask import render_template
from flask import request, redirect, make_response, session
from flask import Flask

from app.controllers.HomeController import homecontroller
from app.controllers.DocumentController import documentcontroller
from app.controllers.InstructorController import instructorcontroller
from app.controllers.SchedulerController import schedulercontroller
from app.helpers.Utility import sendResponse
from app.models.User import user

from Schedule_Linker import getLookup
from random import seed, randint
from functools import wraps
import passwords
import pymongo

front = Blueprint("front", __name__)

testCourses = [
    "20145: CS43203 - Systems Programming", 
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


# Decorators
def login_required(f):
    @wraps(f)
    def wrap(*arg, **kwargs):
        if 'logged_in' in session:
            return f(*arg, **kwargs)
        else:
            return redirect("/login")

    return wrap

def admin_only(f):
    @wraps(f)
    def wrap(*arg, **kwargs):
        if('user_email' in session):
            role = user.getUserRole(session['user_email'])
            if(role != 'ADMIN'):
                return redirect("/denied")
            else:
                return f(*arg, **kwargs)

    return wrap

def scheduler_only(f):
    @wraps(f)
    def wrap(*arg, **kwargs):
        if('user_email' in session):
            role = user.getUserRole(session['user_email'])
            if(role != 'SCHEDULER'):
                return redirect("/denied")
            else:
                return f(*arg, **kwargs)

    return wrap


def prof_only(f):
    @wraps(f)
    def wrap(*arg, **kwargs):
        if('user_email' in session):
            role = user.getUserRole(session['user_email'])
            if(role != 'PROF'):
                return redirect("/denied")
            else:
                return f(*arg, **kwargs)

    return wrap


# Routes
@front.route('/')
@front.route('/login/')
def login_page():
    return render_template("login.html")


@front.route('/login/', methods=['POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

    if user.userExists(email) and passwords.verify_password(password, user.getUserHash(email)):
        role = user.getUserRole(email)
        session = user.startSession(email)

        if(role == "PROF"):
            return redirect("/instructor/")
        elif(role == "ADMIN"):
            return redirect("/administrator/")
        else:
            return redirect("/scheduler/")
    else:
        flash("Incorrect username or password.")
        return redirect("/login")


@front.route('/saveSuccess/<CRN>', methods=['POST'])
def sendInfo(CRN):
    updated_info = {}
    for key in request.form:
        updated_info[key] = request.form[key]

    return instructorcontroller.updateInstructor(session['user_email'], CRN,
            updated_info=updated_info)

@front.route('/instructor/', methods=['GET'])
@front.route('/instructor/<CRN>', methods=['GET'])
@login_required
@prof_only
def instructor(CRN=None):
    if request.method == 'GET':
        return instructorcontroller.getInstructor(session['user_email'], CRN)


@front.route('/administrator/', methods=['GET', 'POST'])
@login_required
@admin_only
def administrator():
    return render_template("administrator.html",
        requiredFields = requiredFields,
        fieldsLen = len(requiredFields)
    )


@front.route('/scheduler/', methods=['GET', 'POST'])
#@login_required
#@scheduler_only
def scheduler():
    if request.method == "GET":
        return schedulercontroller.getSchedule()
    else:
        updated_info = []
        CRN          = request.form.getlist('CRN')
        courseNumber = request.form.getlist('courseNumber')
        section      = request.form.getlist('section')
        courseName   = request.form.getlist('courseName')
        instructor   = request.form.getlist('instructor')
        building     = request.form.getlist('building')
        roomNumber   = request.form.getlist('roomNumber')
        meetingDays  = request.form.getlist('meetingDays')
        meetingTimes = request.form.getlist('meetingTimes')
        for i in len(CRN):
            updated_info.append({
                "CRN"          : CRN[i],
                "courseNumber" : courseNumber[i],
                "section"      : section[i],
                "courseName"   : courseName[i],
                "instructor"   : instructor[i],
                "building"     : building[i],
                "roomNumber"   : roomNumber[i],
                "meetingDays"  : meetingDays[i],
                "meetingTimes" : meetingTimes[i],
                })
        return schedulercontroller.updateSchedule(updated_info)


# Displays register page
@front.route('/register/')
@login_required
def register_page():
    return render_template("register.html")


# Handles register operations
@front.route('/register/', methods=['POST'])
@login_required
def register():
    email = request.form['email']
    password = request.form['password']
    passwordConfirm = request.form['password_confirm']

    if password != passwordConfirm:
        return render_template('register.html')

    password = passwords.encode_password(password)

    if user.userExists(email):
        print(email, " already exists")
    else:
        print(email, " does not exist")

    return redirect("/login")


@front.route('/denied')
def denied():
    return render_template("denied.html")


@front.route('/logout/')
@login_required
def logout():
    session.clear()
    return redirect('/login')

@front.route('/document/docx/<CRN>/', methods=['GET'])
@login_required
@prof_only
def document(CRN):
    return documentcontroller.document(CRN)


@front.route('/document/excel/', methods=['POST'])
#@login_required
#@scheduler_only
def excel():
    try:
        excelDict = documentcontroller.excel(request.files['excelFile'])
    except:
        pass
    return redirect(url_for('front.scheduler'))
