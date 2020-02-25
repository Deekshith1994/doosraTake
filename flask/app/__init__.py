from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

import pyrebase

config = {
    "apiKey": "AIzaSyADrmwSeq9P1XpzxJDmSHUBf6Lz0Fh_lbQ",
    "authDomain": "doosratakedb.firebaseapp.com",
    "databaseURL": "https://doosratakedb.firebaseio.com",
    "projectId": "doosratakedb",
    "storageBucket": "doosratakedb.appspot.com",
    "messagingSenderId": "1031280094205",
    "appId": "1:1031280094205:web:0e943322da317fd143c794",
    "measurementId": "G-T99PD1B4EW"
}

firebase = pyrebase.initialize_app(config)
db1 = firebase.database()

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

from app import views
