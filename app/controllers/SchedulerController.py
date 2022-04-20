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
        # build table entries
        for entry in lookup.getCourses():
            for crn in entry["CRNs"]:
                courseID = lookup.getCourseID(crn)
                coursefile = course.get_data(courseID, crn)
                # build a single row
                CRNs[crn] = {
                        "courseNumber"     : courseID,
                        "Section"          : coursefile["Section"],
                        "Title"            : coursefile["Title"],
                        "instructor-email" : coursefile["instructor-email"],
                        "Building"         : coursefile["Building"],
                        "Room"             : coursefile["Room"],
                        "Meeting Days"     : coursefile["Meeting Days"],
                        "Class Time"       : coursefile["Class Time"],
                    }

        return render_template('scheduler.html',
                CRNs = CRNs,
                CRNsCount = len(CRNs),
                firstRow = False)

    def updateSchedule(self, updated_info):
        # for each course
        for entry in updated_info:
            #update cfields
            crn = entry.pop('CRN', None)
            coursenumber = entry.pop('courseNumber', None)

            course.update_cFields(
                    course_ID=coursenumber,
                    CRN=crn,
                    fields=entry
                )

        return redirect(url_for('front.scheduler'))

schedulercontroller = SchedulerController()
