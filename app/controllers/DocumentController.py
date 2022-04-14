from flask import request
from flask import render_template
from app.helpers.Utility import generateSyllabus,parseExcelFile,sendResponse,getYear,getSemester
from app.models.Course import course

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

        #TODO place the returned dictionary into the database
        for curr in parsedExcelFile:
            print(course.get_file(parsedExcelFile[curr].courseNumber,
                curr))
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
        return ret;

documentcontroller = DocumentController()
