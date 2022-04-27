from flask import Blueprint,request,json, flash
from ..app import mongo
from flask import render_template
from flask import request, redirect, make_response, session, url_for, abort
from flask import Flask

from app.controllers.HomeController import homecontroller
from app.controllers.DocumentController import documentcontroller
from app.controllers.InstructorController import instructorcontroller
from app.controllers.SchedulerController import schedulercontroller
from app.controllers.AdminController import admincontroller
from app.controllers.LoginController import logincontroller
from app.helpers.exceptions import BadRequest
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
    return logincontroller.getLogin()


@front.route('/login/', methods=['POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        return logincontroller.checkLogin(email, password)

@front.route('/updatepassword/')
@login_required
def updatePassword():
    return logincontroller.updatePassword()


@front.route('/updatepassword/', methods=['POST'])
@login_required
def updatePasswordForm():
    password = request.form['password']
    passwordConfirm = request.form['password-confirm']
    ID = session['user_email']

    return logincontroller.updatePasswordPost(password, passwordConfirm, ID)



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
    if request.method == 'GET':
        return admincontroller.getAdmin()
    else:
        updated_info = {}
        for entry in requiredFields:
            temp = request.form.getlist(entry)
            if not temp:
                updated_info[entry] = ""
            else:
                updated_info[entry] = request.form.getlist(entry)[0]

        return admincontroller.setAdmin(updated_info)

@front.route('/scheduler/', methods=['GET', 'POST'])
@login_required
@scheduler_only
def scheduler():
    if request.method == "GET":
        return schedulercontroller.getSchedule()
    else:
        updated_info = []
        CRN          = request.form.getlist('CRN')
        courseNumber = request.form.getlist('courseNumber')
        section      = request.form.getlist('Section')
        courseName   = request.form.getlist('Title')
        instructor   = request.form.getlist('instructor-email')
        building     = request.form.getlist('Building')
        roomNumber   = request.form.getlist('Room')
        meetingDays  = request.form.getlist('Meeting Days')
        meetingTimes = request.form.getlist('Class Time')
        for i in range(0, len(CRN)):
            updated_info.append({
                "CRN"          : CRN[i],
                "courseNumber" : courseNumber[i],
                "Section"      : section[i],
                "Title"        : courseName[i],
                "instructor-email"   : instructor[i],
                "Building"     : building[i],
                "Room"   : roomNumber[i],
                "Meeting Days"  : meetingDays[i],
                "Class Time" : meetingTimes[i],
                })
        return schedulercontroller.updateSchedule(updated_info)


# Displays register page
@front.route('/register/')
@login_required
@admin_only
def register_page():
    return render_template("register.html")


# Handles register operations
@front.route('/register/', methods=['POST'])
@login_required
@admin_only
def register():
    email = request.form['email']
    password = request.form['password']
    passwordConfirm = request.form['password-confirm']
    role = request.form['role-select']

    if user.userExists(email):
        flash("That user already exists.")
        return redirect('/register/')

    if password != passwordConfirm:
        flash("Sorry, the passwords do not match")
        return redirect('/register/')

    if "@kent.edu" not in email:
        flash("Please enter a KSU email.")
        return redirect('/register/')

    password = passwords.encode_password(password)

    user.createUser(ID=email, hash=password, role=role)
    flash("User " + email + " created with role: " + role)
    return redirect('/register/')


@front.route('/remove/')
@login_required
@admin_only
def remove():
    return render_template("removeUser.html")


@front.route('/remove/', methods=['POST'])
@login_required
@admin_only
def removeUser():
    emailToRemove = request.form['email']
    adminPass = request.form['password']

    adminEmail = session['user_email']

    if not user.userExists(emailToRemove):
        flash("Sorry, that user is not in the database")
        return redirect('/remove/')

    if not passwords.verify_password(adminPass, user.getUserHash(adminEmail)):
        flash("Sorry, incorrect password. Please try again")
        return redirect('/remove/')

    if emailToRemove == adminEmail:
        flash("You cannot delete yourself!")
        return redirect('/remove/')

    user.deleteUser(emailToRemove)
    flash("User " + emailToRemove + " has been removed.")
    return redirect('/remove/')


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
@front.route('/document/excel/<REP>', methods=['POST'])
@login_required
@scheduler_only
def excel(REP=''):
    excelDict = {}
    isJson = REP != ''
    try:
        if request.files['excelFile'] is None:
            raise BadRequest
        excelDict = documentcontroller.excel(request.files['excelFile'])
    except BadRequest:
        return abort(400, 'Bad request, expected excelFile') if isJson else flash("Bad request, expected excelFile")
    except pymongo.errors.DuplicateKeyError:
        if isJson:
            return abort(400, 'Provided excel file has already been previously inserted')
        else:
            flash("Provided excel file has already been previously inserted")
    except KeyError:
        if isJson:
            return abort(400, 'Poorly formatted document, please check document format')
        else:
            flash("Poorly formatted document, please check document format")
    except:
        if isJson:
            return abort(400, 'Poorly formatted document, or incorrect type of document')
        else:
            flash("Poorly formatted document, or incorrect type of document")

    # return json if interacting with API
    if isJson:
        return excelDict
    else:
        return redirect(url_for('front.scheduler'))
