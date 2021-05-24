from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://mnfymrkkknsuip:8aa0a12a9e31a42615e39e132e8077c0bbf21c912267ef00c443d08513f7c8a6@ec2-3-215-57-87.compute-1.amazonaws.com:5432/dd3tq83m1u5ukk'
db = SQLAlchemy(app)
bcrypt= Bcrypt(app)
login_manager=LoginManager(app)
login_manager.login_view ='login'
login_manager.login_message_category='info'

from eventPlanr import routes
