from flask import request
from flask import render_template
from app.helpers.Utility import generateSyllabus,parseExcelFile,sendResponse,getYear,getSemester
from app.models.Course import course
from app.models.Lookup import lookup

class DocumentController():

    def __init__(self):
        pass

    def document(self, classCRN):
        return 'hello from document'

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
                    "title"       : parsedExcelFile[curr].title,
                    "section"     : parsedExcelFile[curr].section,
                    "building"    : parsedExcelFile[curr].building,
                    "room"        : parsedExcelFile[curr].room,
                    "time"        : parsedExcelFile[curr].time,
                    "meetingDays" : parsedExcelFile[curr].meetingDays,
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
                        crn= [parsedExcelFile[curr].CRN]
                        )

        return ret;

documentcontroller = DocumentController()
