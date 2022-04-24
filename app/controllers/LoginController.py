from flask import request
from flask import render_template
from flask import send_file
from flask import redirect
from flask import url_for
from flask import flash
import hashlib
import io
import passwords
from app.helpers.Utility   import generateSyllabus,parseExcelFile,sendResponse,getYear,getSemester
from app.models.Course     import course
from app.models.Lookup     import lookup
from app.models.User       import user
from app.helpers.passwords import encode_password

class LoginController():
    def __init__(self):
        pass

    def getLogin(self):
        return render_template("login.html")

    def checkLogin(self, email, password):
        if user.userExists(email) and passwords.verify_password(password, user.getUserHash(email)):
            role = user.getUserRole(email)
            session = user.startSession(email)

            if password == "!WaffleDefault#":
                return redirect("/updatepassword/")

            if(role == "PROF"):
                return redirect("/instructor/")
            elif(role == "ADMIN"):
                return redirect("/administrator/")
            else:
                return redirect("/scheduler/")
        else:
            flash("Incorrect username or password.")
            return redirect("/login/")

    def updatePassword(self):
        return render_template("updatePassword.html")

    def updatePasswordPost(self, password, passwordConfirm, ID):
        if password != passwordConfirm:
            flash("Sorry, the passwords do not match")
            return redirect(url_for('front.updatePassword'))

        role = user.getUserRole(ID)
        user.changePass(ID, passwords.encode_password(password))

        if(role == "PROF"):
            return redirect("/instructor/")
        elif(role == "ADMIN"):
            return redirect("/administrator/")

        return redirect("/scheduler/")


logincontroller = LoginController()
