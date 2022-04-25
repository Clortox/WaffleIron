from flask import request
from flask import render_template
from flask import send_file
from flask import redirect
from flask import url_for
from random import randint
import hashlib
import io
from app.helpers.Utility   import generateSyllabus,parseExcelFile,sendResponse,getYear,getSemester
from app.models.Course            import course
from app.models.Lookup            import lookup
from app.models.User              import user
from app.models.RecomendedPolicy  import recomendedpolicy
from app.helpers.passwords import encode_password

requiredFields = [
    "Kent Core Courses",
    "WIC Courses",
    "Diversity Courses",
    "ELR Courses",
    "Health and Safety",
    "Copyright and Intellectual Property Rights",
    "Registration Requirement",
    "Course Withdrawal Deadlines",
    "Student Accessibility Policy",
    "Student Cheating and Plagiarism",
    "Respectful Student Conduct",
    "Student Survey of Instruction (SSI)"
]

class AdminController():
    def __init__(self):
        pass

    def getAdmin(self):
        # get fields from database
        dbrequiredFields = []
        requiredFieldsLookup = set()
        for policy in recomendedpolicy.getAllPolicy():
            dbrequiredFields.append({
                "pName"       : policy["_id"],
                "policy_data" : policy["policy_data"]
                })
            requiredFieldsLookup.add(policy["_id"])

        for field in requiredFields:
            if field not in requiredFieldsLookup:
                dbrequiredFields.append({
                    "pName"       : field,
                    "policy_data" : ''
                    })

        #return sendResponse(dbrequiredFields)

        return render_template("administrator.html",
            requiredFields = dbrequiredFields,
            fieldsLen = len(requiredFields)
        )

    def setAdmin(self, updated_info):
        #return sendResponse(updated_info)
        for key in updated_info:
            # if the fields exists, update it
            if recomendedpolicy.get_policy(str(key)) != None:
                recomendedpolicy.updaterecpolicydata(
                    pId=str(key),
                    data=updated_info[key],
                    )
            else: #otherwise create it
                recomendedpolicy.addrecpolicy(
                    pID=str(key),
                    pdata=updated_info[key],
                    )


        return redirect(url_for('front.administrator'))

admincontroller=AdminController()
