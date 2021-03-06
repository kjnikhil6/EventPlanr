#import os
#import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect,request,abort
from eventPlanr import app,db,bcrypt,mail
from eventPlanr.forms import RegistrationForm, LoginForm,UpdateAccForm,HostForm,UpdateHostForm
from eventPlanr.models import User, Event
from flask_login import login_user,current_user,logout_user,login_required
import io
from base64 import b64encode
import pytz
from datetime import datetime
from flask_mail import Message


IST=pytz.timezone('Asia/Kolkata')



#decoding image blob data
def img_decoder(imgByt):
    return b64encode(imgByt).decode("utf-8")

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
    hostEvents=sorted(current_user.posts,key= lambda x:x.dateTime)
    joinEvents=sorted(current_user.JoinedEvent,key= lambda x:x.dateTime)
    today=datetime.now(IST).replace(tzinfo=None)
    
    hostEvents=[event for event in hostEvents if event.dateTime>today]
    joinEvents=[event for event in joinEvents if event.dateTime>today]
    yourEvents=hostEvents+joinEvents
    
    schedule=sorted(yourEvents,key= lambda x:x.dateTime)
    #schedule=[event for event in schedule if event.dateTime>today]
    
    upcomingEvents=Event.query.order_by(Event.dateTime).all()
    upcomingEvent5={}
    countr=0
    for event in upcomingEvents:
        if event.dateTime > today and countr < 5:
            if event.banner:
                upcomingEvent5[event]=img_decoder(event.banner)
                countr=countr+1
    
    return render_template('home.html',title='Home',schedule=schedule[:3],upcoming5=upcomingEvent5,hostEvents=hostEvents,joinEvents=joinEvents)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))
 



def save_picture(form_picture,banner=True):
    #random_hex = secrets.token_hex(8)
    #_, f_ext = os.path.splitext(form_picture.filename)
    #picture_fn = random_hex + f_ext
    #picture_path = os.path.join(app.root_path, folder, picture_fn)
    stream=io.BytesIO()
    if banner:
        i = Image.open(form_picture)
        i=i.convert('RGB')
        i.thumbnail((1366,768))
        i.save(stream,format="jpeg")
        imgBytes=stream.getvalue()
        return imgBytes        
    else:
        output_size = (125, 125)
        i = Image.open(form_picture)
        i=i.convert('RGB')
        i.thumbnail(output_size)
        i.save(stream,format="jpeg")
        imgBytes=stream.getvalue()
        return imgBytes


# #encoding image blob if it is to reduced
# def img_encoder_reducer(img,reduce=False):
#     return

    

@app.route('/profile',methods=['GET', 'POST'])
@login_required
def myAccount():
    form=UpdateAccForm()
    if form.validate_on_submit():
        if form.picture.data:
            #picture_file = save_picture(form.picture.data,folder='static/profile_pics')
            imgByte=save_picture(form.picture.data,banner=False)
            #current_user.image_file = form.picture.data.read()
            current_user.image_file=imgByte
        
        current_user.name=form.name.data
        current_user.email=form.email.data
        db.session.commit()
        flash('Your Account has been successfully updated !','success')
        return redirect(url_for('myAccount'))
    elif request.method =='GET':
        form.name.data=current_user.name
        form.email.data =current_user.email   
    #image_file = url_for('static', filename='profile_pics/'+current_user.image_file)
    img_file=img_decoder(current_user.image_file)
    
    hostedEvents=current_user.posts
    joinedEvents=current_user.JoinedEvent
    ConfimredEvents=current_user.ConfirmedEvent
    
    
    return render_template('profile.html',title='myAcc',profile_pic =img_file ,form=form,hostedEvents=hostedEvents,joinedEvents=joinedEvents,ConfimredEvents=ConfimredEvents)


@app.route('/events')
def events():
    all_events=Event.query.order_by(Event.dateTime).all()
    events={}
    today=datetime.now(IST).replace(tzinfo=None)
    for event in all_events:
        if event.dateTime > today:
            if event.banner:
                events[event]=img_decoder(event.banner)
    
 
    
    
    return render_template('EVENTS.html',title='Events',today=today,events=events)

@app.route('/host',methods=['GET', 'POST'])
@login_required
def host():

        form = HostForm()
        if form.validate_on_submit():
            event=Event(title=form.title.data,description=form.description.data,location=form.location.data,dateTime=form.dateTime.data,maxJoin=form.maxJoin.data)
            if form.banner.data:
                
                #to reduce resolution..........
                
                #event.banner=imgByte
                #...........
                #event.banner_file=baner_fil
                #evento=request.files[form.banner.name]
                #event.banner=form.banner.data.read()
                
                imgByte = save_picture(form.banner.data)
                event.banner=imgByte
            
            event.author=current_user
            db.session.add(event)
            db.session.commit()
            flash('Your Event has been created!', 'success')
            return redirect(url_for('home'))

        
        return render_template('hostEvent.html',title='Host',form=form,legend='Host a Event')
 
@app.route('/events/<int:event_id>')
@login_required
def event(event_id):
    event=Event.query.get_or_404(event_id)
    enroll=['Enroll','Enroll in this Event?','Enroll Now','primary',0]
    if event in current_user.JoinedEvent:
        enroll=['Enrolled','UnEnroll from this Event?','UnEnroll','warning',1]
    bannr=img_decoder(event.banner)
    profile_pi=img_decoder(event.author.image_file)
    today=datetime.now(IST).replace(tzinfo=None)
    
    return render_template('EVENT.html',title=event.title,profile_pic=profile_pi,event=event,banner=bannr,enrollVal=enroll,today=today,mail=event.author.mail)

@app.route("/events/<int:event_id>/update", methods=['GET', 'POST'])
@login_required
def update_event(event_id):
    event=Event.query.get_or_404(event_id)
    if event.author != current_user:
        abort(403)
    form = UpdateHostForm()

    if form.validate_on_submit():
        if form.banner.data:
            #banner_fil = save_picture(form.banner.data,reduce=False,folder='static/event_banner')
            #event.banner_file=banner_fil
            event.banner=save_picture(form.banner.data)
        event.title = form.title.data
        event.description = form.description.data
        event.location= form.location.data
        event.dateTime = form.dateTime.data
        event.author.mail=1
        if form.maxJoin.data < len(event.participants):
            db.session.commit()
            flash('All Details Expect No. of Max Participants Was Updated.\n Since '+str(len(event.participants))+' Participants has already been Enrolled','warning')
            return redirect(url_for('event', event_id=event.id))
        else:
            event.maxJoin = form.maxJoin.data
            db.session.commit()
            flash('Your Event has been updated!', 'success')
            return redirect(url_for('event', event_id=event.id))
    elif request.method == 'GET':
        form.title.data = event.title
        form.description.data = event.description
        form.maxJoin.data=event.maxJoin
        form.location.data=event.location
    return render_template('hostEvent.html', title='Update Event',
                           form=form, legend='Update Event')
        
@app.route("/events/<int:event_id>/delete", methods=['POST'])
@login_required
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    if event.author != current_user:
        abort(403)
    db.session.delete(event)
    db.session.commit()
    flash('Your Event has been deleted!', 'success')
    return redirect(url_for('events'))


@app.route("/events/<int:event_id>/join",methods=['POST'])
@login_required
def join_event(event_id):
    event = Event.query.get_or_404(event_id)
    today=datetime.now(IST).replace(tzinfo=None)
    if event.author == current_user :
        flash('Your the Host!!!!!!        ', 'warning')
        return redirect(url_for('events'))
    elif event in current_user.JoinedEvent:
        flash('Already JOINED Event!','warning')
        return redirect(url_for('events'))
    elif len(event.participants) >= int(event.maxJoin):
        flash('The Event is full!! Check again','warning')
        return redirect(url_for('events'))
    
    elif (event.dateTime-today).days < 0:
        flash('Event Expired','danger')
        return redirect(url_for('events'))
        
    else:
        event.participants.append(current_user)
        db.session.commit()
        flash('Successfully Joined the Event!','success')
        return redirect(url_for('event',event_id=event.id)) 
              
    #user = User.query.get(current_user.id)
    #to remove  user.JoinedEvent.remove(event)
    
    
    return "good"
    
@app.route("/events/<int:event_id>/unjoin", methods=['POST'])
@login_required
def unjoin_event(event_id):
    event = Event.query.get_or_404(event_id)
    current_user.JoinedEvent.remove(event)
    db.session.commit()
    flash('You have been successfully unenrolled!', 'success')
    return redirect(url_for('event',event_id=event.id)) 

@app.route("/user_HostEvents/<int:user_id>")
@login_required
def user_HostEvents(user_id):
    user = User.query.get_or_404(user_id)
    
    all_events=user.posts
    all_events=sorted(all_events,key= lambda x:x.dateTime)
    events={}
    today=datetime.now(IST).replace(tzinfo=None)
    
    for event in all_events:
        if event.dateTime > today:
            if event.banner:
                events[event]=img_decoder(event.banner)
    
    
    
    
    return render_template('EVENTS.html',title='Events by'+user.name,today=today,events=events)
    

        
    #joined=Event.query.filter_by(title.data).first()
    #flash('You successfully joined!', 'success')
    #return redirect(url_for('home'))
    
#.......................confirm_mail............
def send_confirm_email(user,event):
    token = user.get_confirm_token(event.id)
    msg = Message('Event Confirmation',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To Confirm your participation in {event.title}, visit the following link:
{url_for('iconfirm', token=token, _external=True)}

This mail has been sent since you have enrolled in {event.title} @eventPlanr.
If you are not able to attend the event then simply ignore this email.
'''
    try:
        mail.send(msg)
    except:
        flash(f'failed to sent confirm mail to {user.email}', 'warning')
        return redirect(url_for('event', event_id=event.id))
        

@app.route("/events/<int:event_id>/send_confirmail",methods=['POST'])
@login_required
def send_confirmail(event_id):
    today=datetime.now(IST).replace(tzinfo=None)
    event = Event.query.get_or_404(event_id)
    if event.author != current_user:
        abort(403)
    elif event.dateTime<today:
        flash('This event has expired', 'danger')
        return redirect(url_for('event', event_id=event.id))
    else:
        users=event.participants
        if len(users)==0:
            flash('No enrolled user to confirm', 'warning')
            return redirect(url_for('event', event_id=event.id))
        event.author.mail=0
        db.session.commit()
        for user in users:
            if user not in event.ConfirmedParticipants:
                send_confirm_email(user,event)
            else:
                continue
        flash('An email has been sent to confirm the participation of enrolled users.', 'info')
        return redirect(url_for('event', event_id=event.id))

@app.route("/iconfirm/<token>")
def iconfirm(token):
    today=datetime.now(IST).replace(tzinfo=None)    
    userEvent = User.verify_confirm_token(token)
    if userEvent is None:
        if current_user.is_authenticated:
            flash('That is an invalid or expired token', 'warning')
            return redirect(url_for('home'))
        else:
            flash('That is an invalid or expired token', 'warning')
            return redirect(url_for('login'))
    user,event=userEvent
    if event.dateTime<today:
        if current_user.is_authenticated:
            flash('The event has expired', 'warning')
            return redirect(url_for('home'))
        else:
            flash('The event has expired', 'warning')
            return redirect(url_for('login'))
    
    elif user in event.ConfirmedParticipants:
         if current_user.is_authenticated:
            flash('You have already confirmed your participation!', 'warning')
            return redirect(url_for('home'))
         else:
             flash('You have already confirmed your participation!', 'warning')
             return redirect(url_for('login'))
    else:
        event.ConfirmedParticipants.append(user)
        db.session.commit()
        if current_user.is_authenticated:
            flash('You have successfully confirmed your participation', 'success')
            return redirect(url_for('home'))
        else:
            flash('You have successfully confirmed your participation', 'success')
            return redirect(url_for('login'))
        

