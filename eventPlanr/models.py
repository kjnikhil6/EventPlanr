from datetime import datetime
from eventPlanr import db,login_manager,app
from flask_login import UserMixin
from eventPlanr.defaultEnc import defaultProfile
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


@login_manager.user_loader
def log_user(user_id):
    return User.query.get(int(user_id))


#database/....................


JoinedUserEvent=db.Table('JoinedUserEvent',
                    db.Column('user_id',db.Integer, db.ForeignKey('user.id')),
                    db.Column('Event_id',db.Integer, db.ForeignKey('event.id')))


ConfirmUserEvent=db.Table('ConfirmUserEvent',
                    db.Column('user_id',db.Integer, db.ForeignKey('user.id')),
                    db.Column('Event_id',db.Integer, db.ForeignKey('event.id')))
                    
                    


class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.LargeBinary, nullable=False, default=defaultProfile)
    password = db.Column(db.String(60), nullable=False)
    mail=db.Column(db.Integer,default=1)
    
    posts = db.relationship('Event', backref='author', lazy=True)
    
    JoinedEvent = db.relationship('Event', secondary=JoinedUserEvent, backref='participants', lazy=True)
    ConfirmedEvent = db.relationship('Event', secondary=ConfirmUserEvent, backref='ConfirmedParticipants', lazy=True)
    
    
    def get_confirm_token(self,event_id,expires_sec=259200):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id,'event_id':event_id}).decode('utf-8')

    @staticmethod
    def verify_confirm_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
            event_id = s.loads(token)['event_id']
        except:
            return None
        return (User.query.get(user_id),Event.query.get(event_id))

    
    
    
    
    
    def __repr__(self):
        return f"User('{self.name}', '{self.email}', '{self.image_file}')"
    
    

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True,nullable=False)
    description = db.Column(db.Text, nullable=False)
    dateTime = db.Column(db.DateTime, nullable=False)

    banner=db.Column(db.LargeBinary,nullable=False)
    #banner_file=db.Column(db.String(50), nullable=False, default='default.jpg')
    
    maxJoin=db.Column(db.Integer,default=100)
    location=db.Column(db.String(100),nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
   
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Event('{self.title}', '{self.description}')"
#..............................
