from flask import Flask,request
from flask_pymongo import PyMongo
import config
import os

app = Flask(__name__, template_folder="views")
#load correct config
if os.environ['FLASK_DEBUG'] == 1:
    cfg = config.Config(os.path.join(os.path.dirname(__file__),'debug.cfg'))
else:
    cfg = config.Config(os.path.join(os.path.dirname(__file__),'production.cfg'))

# setup mongo
app.config['MONGO_DBNAME'] = cfg['MONGO_DBNAME']
app.config['MONGO_URI'] = cfg['MONGO_URI']
mongo = PyMongo(app)

