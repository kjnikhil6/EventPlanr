from datetime import datetime
from eventPlanr import db,login_manager
from flask_login import UserMixin
from eventPlanr.defaultEnc import defaultBanner,defaultProfile


@login_manager.user_loader
def log_user(user_id):
    return User.query.get(int(user_id))


#database/....................


JoinedUserEvent=db.Table('JoinedUserEvent',
                    db.Column('user_id',db.Integer, db.ForeignKey('user.id')),
                    db.Column('Event_id',db.Integer, db.ForeignKey('event.id')))
                    
                    





class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default=defaultProfile)
    password = db.Column(db.String(60), nullable=False)
    
    posts = db.relationship('Event', backref='author', lazy=True)
    
    JoinedEvent = db.relationship('Event', secondary=JoinedUserEvent, backref='participants', lazy=True)
    
    def __repr__(self):
        return f"User('{self.name}', '{self.email}', '{self.image_file}')"


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True,nullable=False)
    description = db.Column(db.Text, nullable=False)
    dateTime = db.Column(db.DateTime, nullable=False)

    banner=db.Column(db.LargeBinary,default=defaultBanner)
    banner_file=db.Column(db.String(50), nullable=False, default='default.jpg')
    
    maxJoin=db.Column(db.Integer,default=100)
    location=db.Column(db.String(100),nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
   
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Event('{self.title}', '{self.description}')"
#..............................