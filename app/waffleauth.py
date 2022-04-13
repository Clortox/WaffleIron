#auth functions are here
#date last modified : 4/6/22

#importing the Firebase Library
from numpy import true_divide
from flask import render_template
import pyrebase

#these are the important API Keys
config = {
  "apiKey": "AIzaSyBAm8I_qmNdtg0JKNBhOg7hPBP1R-NAJKM",
  "authDomain": "waffleiron-da3ca.firebaseapp.com",
  "projectId": "waffleiron-da3ca",
  "storageBucket": "waffleiron-da3ca.appspot.com",
  "databaseURL" : "https://waffleiron-da3ca-default-rtdb.firebaseio.com",
  "messagingSenderId" : "640037946019",
  "appId" : "1:640037946019:web:fe9814956809879c43f516",
  "measurementId": "G-Z71J2Y5G2C"
}

#initializing firebase
firebase = pyrebase.initialize_app(config)

#getting a refernce of firebase auth
auth = firebase.auth()

#functions are here. This is just a draft and will modify soon. We might need to use mongodb to extract user information
def fbsignin(email, password):
    auth.sign_in_with_email_and_password(email, password)
    return render_template("scheduler.html")

def signup(email, password):
    return auth.create_user_email_and_password(email, password)

def confirmpassword(password, cpassword):
    if(password == cpassword):
      return True
    else:
      return False