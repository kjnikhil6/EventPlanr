from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://wgathkgilknakc:e1c5d33d3b99038d6cb49c64cba5e1b7386c6b13e94f41c8b615fb3185a4384a@ec2-52-0-114-209.compute-1.amazonaws.com:5432/d5pn0s9rcig3i6'
db = SQLAlchemy(app)
bcrypt= Bcrypt(app)
login_manager=LoginManager(app)
login_manager.login_view ='login'
login_manager.login_message_category='info'

from eventPlanr import routes
