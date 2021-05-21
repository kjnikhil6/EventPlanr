import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect,request
from eventPlanr import app,db,bcrypt
from eventPlanr.forms import RegistrationForm, LoginForm,UpdateAccForm,HostForm
from eventPlanr.models import User, Event
from flask_login import login_user,current_user,logout_user,login_required




@app.route('/')
def hello():
    
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    return render_template('intro.html')

@app.route('/login',methods=['GET', 'POST'])
def login():
    
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    
    form = LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email & password', 'danger')
    return render_template('LOGIN.html',title='Log In',form=form)
@app.route('/signup',methods=['GET', 'POST'])
def signUp():
    
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user=User(name=form.name.data,email=form.email.data,password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('signUP.html',title='Register',form=form)


@app.route('/home')
def home():
    return render_template('home2.html',title='Home')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))
 



def save_picture(form_picture,reduce=True,folder=""):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, folder, picture_fn)
    
    if reduce:
        output_size = (125, 125)
        i = Image.open(form_picture)
        i.thumbnail(output_size)
        i.save(picture_path)
    else:
        form_picture.save(picture_path)

    return picture_fn

@app.route('/profile',methods=['GET', 'POST'])
@login_required
def myAccount():
    form=UpdateAccForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data,folder='static/profile_pics')
            current_user.image_file = picture_file
        current_user.name=form.name.data
        current_user.email=form.email.data
        db.session.commit()
        flash('Your Account has been successfully updated !','success')
        return redirect(url_for('myAccount'))
    elif request.method =='GET':
        form.name.data=current_user.name
        form.email.data =current_user.email   
    image_file = url_for('static', filename='profile_pics/'+current_user.image_file)
    return render_template('profile.html',title='myAcc',image_file =image_file ,form=form)

@app.route('/events')
def events():
    all_events=Event.query.all()
    return render_template('events.html',title='Events',events=all_events)

@app.route('/host',methods=['GET', 'POST'])
@login_required
def host():

        form = HostForm()
        if form.validate_on_submit():
            event=Event(title=form.title.data,description=form.description.data,location=form.location.data,dateTime=form.dateTime.data,maxJoin=form.maxJoin.data)
            if form.banner.data:
                banner_fil = save_picture(form.banner.data,reduce=False,folder='static/event_banner')
                event.banner_file=banner_fil
            event.author=current_user
            db.session.add(event)
            db.session.commit()
            flash('Your Event has been created!', 'success')
            return redirect(url_for('host'))

        
        return render_template('hostEvent.html',title='Host',form=form)
 
@app.route('/events/<int:event_id>')

def event(event_id):
    event=Event.query.get_or_404(event_id)
    return render_template('EVENT.html',title=event.title,event=event)

@app.route('/events/join',methods=['POST'])
def join():
    #joined=Event.query.filter_by(title.data).first()
    flash('You successfully joined!', 'success')
    return redirect(url_for('home'))