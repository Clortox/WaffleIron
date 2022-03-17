from flask import Blueprint,request,json
from flask_pymongo import ObjectId
from ..app import mongo
from flask import render_template
from app.controllers.HomeController import homecontroller

front = Blueprint("front", __name__)

testCourses = {20145: "CS43203 - Systems Programming", 
               12412: "CS49999 - Capstone", 
               12393: "CS45203 - Computer Network Security"}
defaultFields = [
    "Course Times",
    "Contact Information",
    "Course Description",
    "Prerequisites",
    "Kent Core Fulfillments",
    "Learning Outcomes",
    "Grading Scale",
    "Attendance Policy",
    "Course Schedule"
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