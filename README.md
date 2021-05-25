![BFH Banner](https://trello-attachments.s3.amazonaws.com/542e9c6316504d5797afbfb9/542e9c6316504d5797afbfc1/39dee8d993841943b5723510ce663233/Frame_19.png)
# eventPlanr
eventPlanr: [https://eventplanr.herokuapp.com/]
-----With eventPlanr User can create His/Her account and Host/Enroll in Events.

*User is able to sign up,signin,create/join event,and logout.
*User's Home page consists of schedule for notifying His/Her Upcoming Events(joined&hosted),
      a slideshow containing details of latest 5 upcoming events.
*A profile page is provided where user can update his details and upload profile picture,
      a dashboard is provided to view his joined/hosted events.
*User can host events By filling in details(title,description,banner,date,location....)
*A option to update/delete the hosted events is given to the host.
*the host can view the details of participants 
*User can view all upcoming events and enroll 
*Non-Signedin users can also view the ongoing events
*Added rvsp module to confirm participation of users(by send mail to enrolled users)


## Team members
1. NIKHIL K J [https://github.com/kjnikhil6]
2. MUHAMMED JASEEM TP[https://github.com/jaseem-tp]
## Team Id
 BFH/rec5uIVbgp7fzhDf4/2021
## Link to product walkthrough
[https://youtu.be/CHJhkNrKqV0]
## How it Works ?
1) Visit  https://eventplanr.herokuapp.com/
2) Click on SignUp option in the navigation  bar and fill in details to signup.
3) By SigningUp you will redirected to login page, enter email,password to login.
4) After loging in you will be Directed to homepage,
       Here you can see a slideshow of latest 5 upcoming events,
       a schedule to notify your upcoming events
5) You can JOin/host events by clicking JOIN EVENTS/HOST EVENTS icon on navigation bar
6) By clicking on join events you will be directed to events page where all the hosted events are posted(sorted by date of the event)
7) if you are interested in a particular event,click on 'VIEW' button .
8) by clicking the 'VIEW' button,you  can see that events details,no.of participants joined
     and an option to enroll in the event is provided.
9) by clcking on enroll button you can join the event.
10)if you wish to host,click on host events in navigation bar and fill the form.
11)your joined and hosted events can be seen in homepage&profile page.
12)in the profile page(by clciking on 'myAccount' in navigation bar) you update details and upload profile picture
13)if you join/host event the schedule in home page will display your latest 3 upcoming event in sorted way.
## Libraries used
flask==1.1.2
flask-bcrypt==0.7.1
flask-login==0.5.0
flask-mail==0.9.1
flask-sqlalchemy==2.5.1
flask-wtf==0.14.3
gunicorn==20.0.4
itsdangerous==1.1.0
jinja2==2.11.2
markupsafe==1.1.1
pillow==8.0.1
psycopg2-binary
pycodestyle==2.6.0
python-dateutil==2.8.1
python-editor==1.0.4
pytz==2020.1
werkzeug==1.0.1
wtforms==2.2.1
## How to configure
Instructions for setting up project

1)clone the github repo to your local machine
2)pip install the files in "requirements.txt"
3)add environment variable to store email address and password and call the variables in init.py file
4)open terminal(cmd) and change directory to the folder where you cloned the github repo
5)then type 
    >>>"from eventPlanr import db"
    >>>"db.create_all()"
  the above commands is to create the database "site.db" in your directory


## How to Run
open and run "app.py"


