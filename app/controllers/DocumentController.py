from flask import request
from flask import render_template
from app.helpers.Utility import generateSyllabus,parseExcelFile

class DocumentController():

    def __init__(self):
        pass

    def document(self, classCRN):
        return 'Hello from Document ' + classCRN

    def excel(self, excel_file):
        return {'Message' : "Hello from excel"}
        pass

documentcontroller = DocumentController()
