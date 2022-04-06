import pyrebase

config = {
  "apiKey": "apiKey",
  "authDomain": "projectId.firebaseapp.com",
  "databaseURL": "https://databaseName.firebaseio.com",
  "storageBucket": "projectId.appspot.com",
  "serviceAccount": "path/to/serviceAccountCredentials.json"
}

firebase = pyrebase.initialize_app(config)

auth = firebase.auth()

def signin():
    return auth.sign_in_with_user_password(email, password)

def signup():
    return auth.create_user_email_and_password(email, password)