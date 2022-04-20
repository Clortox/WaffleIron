from flask import request
from flask import render_template
from flask import send_file
from flask import redirect
from flask import url_for
import hashlib
import io
from app.helpers.Utility   import generateSyllabus,parseExcelFile,sendResponse,getYear,getSemester
from app.models.Course     import course
from app.models.Lookup     import lookup
from app.models.User       import user
from app.helpers.passwords import encode_password

class SchedulerController():
    def __init__(self):
        pass

    def getSchedule(self):
        CRNs = {}
        for entry in lookup.getCourses():
            for crn in entry["CRNs"]:
                courseID = lookup.getCourseID(crn)
                coursefile = course.get_data(courseID, crn)
                CRNs[crn] = {
                        "courseNumber" : courseID,
                        "section"      : coursefile["Section"],
                        "courseName"   : coursefile["Title"],
                        "instructorEmail" : coursefile["instructor-email"],
                        "building"        : coursefile["Building"],
                        "roomNumber"      : coursefile["Room"],
                        "meetingDays"     : coursefile["Meeting Days"],
                        "meetingTime"     : coursefile["Class Time"],
                    }

        return render_template('scheduler.html',
                CRNs = CRNs,
                CRNsCount = len(CRNs),
                firstRow = False)

    def updateSchedule(self, updated_info):
        for entry in update_info:
            #TODO insert values from update_info into database
            pass

        pass
schedulercontroller = SchedulerController()
