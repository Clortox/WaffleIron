from flask import request
from flask import render_template
from app.helpers.Utility import generateSyllabus,parseExcelFile,sendResponse

class DocumentController():

    def __init__(self):
        pass

    def document(self, classCRN):
        return 'Hello from Document ' + classCRN

    def excel(self, excel_file):
        parsedExcelFile = parseExcelFile(excel_file)
        ret = {}
        for key in parsedExcelFile:
            ret[key] = parsedExcelFile[key].serialize()

        #TODO place the returned dictionary into the database

        return ret

documentcontroller = DocumentController()
