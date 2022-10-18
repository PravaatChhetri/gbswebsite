from flask import Flask, redirect, url_for, render_template, request,session
from flask_sqlalchemy import SQLAlchemy
from models import userInfo, Grounds, Bookings, Blogs
import forms as f
import functions as func
# from db import db_init,db
import http.client
import json
import requests
from datetime import datetime



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gbsDB.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)
app.config['SECRET_KEY'] = 'groundbookingsystem'

class userInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    role = db.Column(db.String(10), nullable=False)
    dy = db.Column(db.String(10), nullable=True)
    password=db.Column(db.String(100),nullable=False)

    # def __init__(self, email, role, dy,password):
    #     self.email = email
    #     self.role = role
    #     self.dy = dy
    #     self.password=password

class Grounds(db.Model):
    gId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    groundName = db.Column(db.String(100), unique=True, nullable=False)
    NoOfCourt = db.Column(db.Integer, nullable=False)
    bookTime = db.Column(db.Float, nullable=False)

    # def __init__(self, groundName, NoOfCourt, bookTime):
    #     self.groundName = groundName
    #     self.NoOfCourt = NoOfCourt
    #     self.bookTime = bookTime

class Bookings(db.Model):
    bId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ground = db.Column(db.String(100), nullable=False)
    team_1 = db.Column(db.String(10), nullable=False)
    team_2 = db.Column(db.String(10), nullable=False)
    courtName = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.String(100), nullable=False)

    # def __init__(self, ground, team_1, team_2, courtName, date, time):
    #     self.ground = ground
    #     self.team_1 = team_1
    #     self.team_2 = team_2
    #     self.courtName = courtName
    #     self.date = date
    #     self.time = time

class Blogs(db.Model):
    BId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String, nullable=False)
    author = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String, nullable=False)
    mimetype = db.Column(db.String, nullable=False)
    date_created = db.Column(
    db.DateTime, nullable=False, default=datetime.utcnow)

    # def __init__(self, title, content, author, image, mimetype):
    #     self.title = title
    #     self.content = content
    #     self.author = author
    #     self.image = image
    #     self.mimetype = mimetype
    


course=[' 1Arch ',' 1CE ',' 1ECE ',' 1EE ',' 1EG ',' 1ICE ',' 1IT ',' 2Arch ',' 2CE ',' 2ECE ',' 2EE ',' 2EG ',' 2ICE ',' 2IT ',' 3Arch ',' 3CE ',' 3ECE ',' 3EE ',' 3EG ',' 3ICE ',' 3IT ',' 4Arch ',' 4CE ',' 4ECE ',' 4EE ',' 4EG ',' 4ICE ',' 4IT ',' 5Arch ']
court=[]

role_status='Admin'


@app.route('/')
def home():
    news = api()
    val = {'news': news, 'a': 'active', 'role_status': role_status}
    return render_template('home.html', data=val)


@app.route('/blog')
def blog():
    return render_template('blog.html', data={'b': 'active','role_status': role_status})



@app.route('/booking')
def booking():
    return render_template('booking.html', data={'d': 'active','role_status': role_status})


@app.route('/gamesCouncillor-Dashboard', methods=['POST', 'GET'])
def admin():
    if True:
    #if 'role' in session:
        email =None 
        role = None
        dept = None
        year = None
        title=None
        content=None
        author=None
        blogPic=None
        groundName=None
        NoOfCourt=None
        bookTime=None
        GroundName=None
        courtName=None
        team_1=None
        team_2=None
        date=None
        time=None
        password = 'Cst@12345'

        reg=f.RegistrationForm()
        reg.role.choices=['Class Representative','Staff']
        reg.year.choices=['1','2','3','4','5']
        reg.dept.choices=['Arch','CE','ECE','EE','EG','ICE','IT']
        blog=f.BlogForm()
        Ground=f.GroundForm()
        booking=f.BookingForm()
        booking.courtName.choices=func.court(3)
        booking.time.choices=func.schedule(1)
        booking.team_1.choices=course
        booking.team_2.choices=course


        register={'reg':reg,'email':email,'role':role,'dept':dept,'year':year}
        b={'blog':blog,'title':title,'content':content,'author':author,'blogPic':blogPic}
        G={'Ground':Ground,'groundName':groundName,'NoOfCourt':NoOfCourt,'bookTime':bookTime}
        bk={'booking':booking,'GroundName':GroundName,'courtName':courtName,'date':date,'time':time}
        detail={'register':register,'b':b,'G':G,'bk':bk}
        if request.method == 'POST':
            if reg.validate_on_submit():
                email = reg.email.data
                role = reg.role.data
                dept = reg.dept.data
                year = reg.year.data
                dy=year+dept
                print(email,role,dy,password)
                r=userInfo(email=email,role=role,dy=dy,password=password)
                db.session.add(r)
                db.session.commit()

                reg.email.data=''
                reg.role.data=''
                reg.dept.data=''
                reg.year.data=''
                
            if blog.validate_on_submit():
                title=blog.title.data
                content=blog.content.data
                author=blog.author.data
                blogPic=blog.upload.data
                mimetype=''
                img=''
                if blogPic:
                    mimetype=blogPic.mimetype
                    img=blogPic.read()
                blog=Blogs(title=title,content=content,author=author,mimetype=mimetype,image=img)
                db.session.add(blog)
                db.session.commit()
                
                print(title,content,author,blogPic)  
                blog.title.data=''
                blog.content.data=''
                blog.author.data=''
                blog.upload.data=''    
            if Ground.validate_on_submit():
                groundName=Ground.groundName.data
                NoOfCourt=Ground.NoOfCourt.data
                bookTime=Ground.bookTime.data
            
                g=Grounds(groundName=groundName,NoOfCourt=NoOfCourt,bookTime=bookTime)
                db.session.add(g)
                db.session.commit()
                print(groundName,NoOfCourt,bookTime)
                Ground.groundName.data=''
                Ground.NoOfCourt.data=''
                Ground.bookTime.data=''
            if booking.validate_on_submit():
                GroundName=booking.groundName.data
                courtName=booking.courtName.data
                team_1=booking.team_1.data
                team_2=booking.team_2.data
                date=booking.date.data
                time=booking.time.data
                
                b=Bookings(GroundName=GroundName,courtName=courtName,team_1=team_1,team_2=team_2,date=date,time=time)
                db.session.add(b)
                db.session.commit()

                print(GroundName,courtName,team_1,team_2,date,time)
                booking.groundName.data=''
                booking.courtName.data=''
                booking.team_1.data=''
                booking.team_2.data=''
                booking.date.data=''
                booking.time.data=''
            
        return render_template('admin_page.html',detail=detail,data={'f':'active','role_status': role_status})
    else:
        return redirect(url_for('login'))

@app.route('/User-Dashboard')
def studentDash():
    if True:
    #if "role" in session:
        GroundName=None
        courtName=None
        team_1=None
        team_2=None
        date=None
        time=None
        booking=f.BookingForm()
        booking.courtName.choices=func.court(3)
        booking.time.choices=func.schedule(1)
        booking.team_1.choices=course
        booking.team_2.choices=course
        bk={'booking':booking,'GroundName':GroundName,'courtName':courtName,'date':date,'time':time}
        detail={'bk':bk}
        if booking.validate_on_submit():
            GroundName=booking.groundName.data
            courtName=booking.courtName.data
            team_1=booking.team_1.data
            team_2=booking.team_2.data
            date=booking.date.data
            time=booking.time.data
            print(GroundName,courtName,team_1,team_2,date,time)
            booking.groundName.data=''
            booking.courtName.data=''
            booking.team_1.data=''
            booking.team_2.data=''
            booking.date.data=''
            booking.time.data=''

        return render_template('userDash.html', data={'g':'active','role_status': role_status},detail=detail)
    else:
        return redirect(url_for('login'))


@app.route('/aboutUs')
def aboutUs():
    return render_template('about_us.html', data={'e': 'active','role_status': role_status})


@app.route('/login', methods=['POST', 'GET'])
def login():
    email = None
    password = None
    form = f.LoginForm()
    if request.method == 'POST':
       
        if form.validate_on_submit():
            session['role']='Admin'
            email = form.email.data
            password = form.password.data
            form.email.data = ''
            form.password.data = ''
            print(email,password)
    return render_template('login.html', data={'f': 'active','role_status': role_status}, form=form, email=email, password=password)

def api():
    url = ('https://newsapi.org/v2/top-headlines?'
           'country=in'
           '&category=sports'
           '&apiKey=f36c80f9c4e041a48e37a202d089ea13')
    raesponse = requests.get(url)
    return raesponse.json()['articles']
     
def logout():
    session.pop('role', None)
    return redirect(url_for('login'))

with app.app_context():
    db.create_all()
    

if __name__ == "__main__":
    app.run(debug=True)
