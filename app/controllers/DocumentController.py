from flask import request
from flask import render_template
from flask import send_file
import hashlib
import io
from app.helpers.Utility         import generateSyllabus,parseExcelFile,sendResponse,getYear,getSemester
from app.models.Course           import course
from app.models.Lookup           import lookup
from app.models.User             import user
from app.models.RecomendedPolicy import recomendedpolicy
from app.helpers.passwords import encode_password

class DocumentController():

    def __init__(self):
        pass

    def document(self, classCRN):
        # get info needed for generateSyllabus call
        # get course information
        courseID = lookup.getCourseID(classCRN)
        courseData = course.get_file(
                course_ID=courseID,
                CRN=classCRN)

        # get professor
        prof = user.getUserContact(str(courseData["cFields"]["instructor-email"]))

        # get required fields
        reqfields = recomendedpolicy.getAllPolicy()

        syllabus = generateSyllabus(
                professor=prof,
                course=courseData,
                CRN=classCRN,
                reqfields=reqfields)

        buffer = io.BytesIO()
        syllabus.save(buffer)
        buffer.seek(0)

        return send_file(
                path_or_file=buffer,
                #mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                download_name="Syllabus_" + classCRN + ".docx",
                as_attachment=True,
                )

    def excel(self, excel_file):
        parsedExcelFile = parseExcelFile(excel_file)
        ret = {}
        for key in parsedExcelFile:
            ret[key] = parsedExcelFile[key].serialize()

        #place the returned dictionary into the database
        for curr in parsedExcelFile:
            print(course.get_file(parsedExcelFile[curr].courseNumber,
                curr))
            # place into the courses table
            course.createFile(
                cID=parsedExcelFile[curr].courseNumber,
                CRN=parsedExcelFile[curr].CRN,
                cYear=getYear(),
                cSem=getSemester(),
                data={
                    "Title"                  : parsedExcelFile[curr].title,
                    "Section"                : parsedExcelFile[curr].section,
                    "Building"               : parsedExcelFile[curr].building,
                    "Room"                   : parsedExcelFile[curr].room,
                    "Class Time"             : parsedExcelFile[curr].time,
                    "Meeting Days"           : parsedExcelFile[curr].meetingDays,
                    "instructor-email"       : parsedExcelFile[curr].instructorEmail,
                    "instructor-name"        : parsedExcelFile[curr].instructorName,
                }
            )

            #place into the lookup table
            # first check if course ID is in the lookup table
            # its in the lookup table, therefore we only need to add the CRN
            if lookup.getCourseName_cID(parsedExcelFile[curr].courseNumber) != 'ER404':
                lookup.addCourseCRN(
                        cID=parsedExcelFile[curr].courseNumber,
                        CRN=parsedExcelFile[curr].CRN)
            else:
                #otherwise add new entry to the lookup table
                lookup.addCourse(
                        ID=parsedExcelFile[curr].courseNumber,
                        name=parsedExcelFile[curr].title,
                        crn= [parsedExcelFile[curr].CRN])

            # add CRN to professor
            # if professor exists, only add the CRN
            if parsedExcelFile[curr].instructorEmail != '' and \
                user.userExists(parsedExcelFile[curr].instructorEmail):
                user.addCRN(
                        ID=parsedExcelFile[curr].instructorEmail,
                        crn=parsedExcelFile[curr].CRN)
            elif parsedExcelFile[curr].instructorEmail != '':
                #otherwise add new instructor
                user.createUser(
                        ID=parsedExcelFile[curr].instructorEmail,
                        hash=encode_password('!WaffleDefault#'),
                        contact = {
                            "email" : parsedExcelFile[curr].instructorEmail,
                            "name"  : parsedExcelFile[curr].instructorName
                            },
                        crn=[parsedExcelFile[curr].CRN]
                        )

        return ret;

documentcontroller = DocumentController()
