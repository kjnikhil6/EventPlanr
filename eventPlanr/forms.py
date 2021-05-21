from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField,BooleanField,IntegerField,TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo,ValidationError
from eventPlanr.models import User,Event
from dateutil.parser import parse 
from datetime import datetime

class RegistrationForm(FlaskForm):
    name = StringField('Name',validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password')])
    
    submit = SubmitField('SignUp')
    
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email has already been taken')


    
    

class LoginForm(FlaskForm):
        email = StringField('Email',validators=[DataRequired(), Email()])
        password = PasswordField('Password', validators=[DataRequired()])
        remember = BooleanField('Remember Me')
        submit = SubmitField('Login')


class UpdateAccForm(FlaskForm):
    name = StringField('Name',validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',validators=[DataRequired(), Email()])
    
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    
    submit = SubmitField('Update')
    
    
   
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email has already been taken')
                
class HostForm(FlaskForm):
    
    title = StringField('Event Title',validators=[DataRequired(), Length(min=3, max=40)])
    description=TextAreaField('Description',validators=[DataRequired(), Length(min=3, max=5000)])
    dateTime =  StringField('Event Date&Time',validators=[DataRequired()])
    location = StringField('Event Location',validators=[DataRequired(), Length(min=3, max=20)])
    banner = FileField('Event Banner', validators=[FileAllowed(['jpg', 'png'])])
    maxJoin = IntegerField('Max No.of Participants')
    
    submit = SubmitField('Host')
    
    def validate_dateTime(self, dateTime):
        if dateTime.data:
            if parse(dateTime.data) < datetime.utcnow():
                raise ValidationError('Select an Upcoming Date')
            else:
                dateTime.data=parse(dateTime.data)
            
            # else:
            #     dateTime.data=d 
    
    def validate_title(self, title):
            t = Event.query.filter_by(title=title.data).first()
            if t:
                raise ValidationError('Title has already been taken')
    
    def validate_maxJoin(self, maxJoin):

        if  maxJoin.data :
            if maxJoin.data < 4:
                raise ValidationError('There should be atleast 4 participants!')
               