#auth functions are here
#date last modified : 4/6/22

#importing the Firebase Library
from numpy import true_divide
import pyrebase

#these are the important API Keys
config = {
  "apiKey": "apiKey",
  "authDomain": "projectId.firebaseapp.com",
  "databaseURL": "https://databaseName.firebaseio.com",
  "storageBucket": "projectId.appspot.com",
  "serviceAccount": "path/to/serviceAccountCredentials.json"
}

#initializing firebase
firebase = pyrebase.initialize_app(config)

#getting a refernce of firebase auth
auth = firebase.auth()

#functions are here. This is just a draft and will modify soon. We might need to use mongodb to extract user information
def signin(email, password):
    return auth.sign_in_with_user_password(email, password)

def signup(email, password):
    return auth.create_user_email_and_password(email, password)

def confirmpassword(password, cpassword):
    if(password == cpassword):
      return True
    else:
      return False