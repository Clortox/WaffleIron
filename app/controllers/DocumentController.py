from flask import request
from flask import render_template
from flask import send_file
import hashlib
import io
from app.helpers.Utility import generateSyllabus,parseExcelFile,sendResponse,getYear,getSemester
from app.models.Course import course
from app.models.Lookup import lookup
from app.models.User   import user

class DocumentController():

    def __init__(self):
        pass

    def document(self, classCRN):
        # get info needed for generateSyllabus call
        # get course information
        courseID = lookup.getCourseID(int(classCRN))
        courseData = course.get_file(
                course_ID=int(courseID),
                CRN=int(classCRN))

        # get professor
        prof = user.getUserContact(str(courseData["cFields"]["instructorEmail"]))


        syllabus = generateSyllabus(
                professor=prof,
                course=courseData,
                CRN=classCRN)

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
                    "title"           : parsedExcelFile[curr].title,
                    "section"         : parsedExcelFile[curr].section,
                    "building"        : parsedExcelFile[curr].building,
                    "room"            : parsedExcelFile[curr].room,
                    "time"            : parsedExcelFile[curr].time,
                    "meetingDays"     : parsedExcelFile[curr].meetingDays,
                    "instructorEmail" : parsedExcelFile[curr].instructorEmail
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
                        hash=hashlib.sha256(b'password').hexdigest(),
                        contact = {
                            "email" : parsedExcelFile[curr].instructorEmail,
                            "name"  : parsedExcelFile[curr].instructorName
                            },
                        crn=[parsedExcelFile[curr].CRN]
                        )

        return ret;

documentcontroller = DocumentController()
