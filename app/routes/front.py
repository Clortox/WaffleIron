from flask import Blueprint,request,json
from flask_pymongo import ObjectId
from ..app import mongo
from flask import render_template
from app.controllers.HomeController import homecontroller

front = Blueprint("front", __name__)

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
    return render_template("scheduler.html"
    )

@front.route('/document/docx/<CRN>', methods=['GET'])
def document(CRN):
    return 'Hello from document! ' + CRN

@front.route('/document/excel/', methods=['POST'])
def excel():
    f = request.files['file']
    return 'file uploaded'
