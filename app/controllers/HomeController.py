from flask import request
from flask import render_template
from app.helpers.Utility import sendResponse

class HomeController():

    def __init__(self):
        pass

    def index(self):
        return render_template('index.html')

homecontroller = HomeController()
