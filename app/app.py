from flask import Flask,request
from pymongo import MongoClient
import config
import os

app = Flask(__name__, template_folder="views")
app.secret_key = b'\xa0\x82\x86r\x8e \xb7RR\xf4\x8cw\xeax\xa7\x90\xec\xc9*\xb6\x97\xb5\x80\xa7\x82m\x88\xc4\xf7\xb51\x96'

#load correct config
if os.environ['FLASK_DEBUG'] == 1:
    cfg = config.Config(os.path.join(os.path.dirname(__file__),'debug.cfg'))
else:
    cfg = config.Config(os.path.join(os.path.dirname(__file__),'production.cfg'))

# setup mongo
#app.config['MONGO_DBNAME'] = cfg['MONGO_DBNAME']
#app.config['MONGO_URI'] = cfg['MONGO_URI']

mongo = MongoClient(cfg['MONGO_URI'])[cfg['MONGO_DBNAME']]
