#auth functions are here
#date last modified : 4/6/22

#importing the Firebase Library
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
def signin():
    return auth.sign_in_with_user_password(email, password)

def signup():
    return auth.create_user_email_and_password(email, password)