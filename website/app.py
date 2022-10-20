import sqlite3
from flask import Flask, redirect, url_for, render_template, request,session,Response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from models import userInfo, Grounds, Bookings, Blogs
import forms as f
import functions as func
from db import db_init,db
import http.client
import json
import requests
from datetime import datetime



app = Flask (__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gbsDB.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'groundbookingsystem'

db_init(app)

course=[' 1Arch ',' 1CE ',' 1ECE ',' 1EE ',' 1EG ',' 1ICE ',' 1IT ',' 2Arch ',' 2CE ',' 2ECE ',' 2EE ',' 2EG ',' 2ICE ',' 2IT ',' 3Arch ',' 3CE ',' 3ECE ',' 3EE ',' 3EG ',' 3ICE ',' 3IT ',' 4Arch ',' 4CE ',' 4ECE ',' 4EE ',' 4EG ',' 4ICE ',' 4IT ',' 5Arch ']
court=[]


role_status='None'


@app.route('/')
def home():
    news = api()
    val = {'news': news,'role_status':session['LogAs'], 'a': 'active'}
    return render_template('home.html', data=val)


@app.route('/blog')
def blog():
    _blogs=Blogs.query.order_by(Blogs.date_created).all()
    return render_template('blog.html', data={'b': 'active','role_status':session['LogAs'],'blogs':_blogs})

@app.route('/editBlog/<int:id>',methods=['GET','POST'])
def editGivenBlog(id):
    if session['LogAs']=='Admin':
        form=f.BlogForm()
        _blog=Blogs.query.filter_by(BId=id).first()
        form.content.data = _blog.content
        b={'blog':form}
        detail={'b':b,'bb':_blog}
        if request.method=='POST':
            blogPic=form.upload.data
            if blogPic:
                _blog.mimetype=blogPic.mimetype
                _blog.image=blogPic.read()
            _blog.title=form.title.data
            _blog.content=form.content.data
            _blog.author=form.author.data
            db.session.commit()
            return redirect(url_for('blog'))
        return render_template('editGivenBlog.html',data={'role_status': session['LogAs']},detail=detail)
    else:
        return redirect(url_for('login'))


@app.route('/deleteBlog/<int:id>')
def deleteBlog(id):
    if session['LogAs']=='Admin':
        _blog=Blogs.query.filter_by(BId=id).first()
        db.session.delete(_blog)
        db.session.commit()
        return redirect(url_for('blog'))
    else:
        return redirect(url_for('login'))

@app.route('/blog/img/<int:id>')
def get_img(id):
    img=Blogs.query.filter_by(BId=id).first()
    return Response(img.image,mimetype=img.mimetype)
    

@app.route('/blog/<int:id>')
def blog_detail(id):
        
    blog=Blogs.query.filter_by(BId=id).first()
    return render_template('blog_disp.html', data={'b': 'active','role_status':session['LogAs'],'blog':blog})
    

@app.route('/booking')
def booking():
    _booking=Bookings.query.order_by(Bookings.date).all()
    return render_template('booking.html', data={'d': 'active','role_status':session['LogAs'],'bookings':_booking}) 



@app.route('/editBooking/<int:id>',methods=['GET','POST'])
def editB(id):
    if 'role' in session:
        form=f.BookingForm()
        g=Grounds.query.all()
        ground=[]
        for x in g:
            ground.append(x.groundName)
        form.groundName.choices=ground
        form.courtName.choices=func.court(3)
        form.time.choices=func.schedule(1)
        form.team_1.choices=course
        form.team_2.choices=course
        
        uData=Bookings.query.get_or_404(id)
        bk={'booking':form}
        detail={'bk':bk,'uData':uData}
        if request.method == 'POST':
            checkBook=Bookings.query.all()
            for x in checkBook:
                if(x.ground==form.groundName.data and x.courtName==form.courtName.data and x.date==form.date.data and x.time==form.time.data):
                    print("Booking has been already made")
                    return redirect('/gamesCouncillor-Dashboard')     
            uData.groundName=form.groundName.data
            uData.team_1=form.team_1.data
            uData.team_2=form.team_2.data
            uData.courtName=form.courtName.data
            uData.date=form.date.data
            uData.time=form.time.data
            db.session.commit()
            return redirect('/booking')
        else:
            return render_template('editGivenBooking.html',data={'role_status': session['LogAs']},detail=detail)
    else:
        return redirect('/login')

@app.route('/deleteBooking/<int:id>')
def deleteB(id):
    if 'role' in session:
        uData=Bookings.query.get_or_404(id)
        db.session.delete(uData)
        db.session.commit()
        return redirect('/booking')
    return redirect('/login')


@app.route('/gamesCouncillor-Dashboard', methods=['POST', 'GET'])
def admin():
    if 'role' in session:
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
        g=Grounds.query.all()
        ground=[]
        for x in g:
            ground.append(x.groundName)
        booking.groundName.choices=ground
        booking.courtName.choices=func.court(3)
        booking.time.choices=func.schedule(1)
        booking.team_1.choices=course
        booking.team_2.choices=course
        _booking=Bookings.query.order_by(Bookings.date).all()
        _blogs=Blogs.query.order_by(Blogs.date_created).all()   



   
        register={'reg':reg,'email':email,'role':role,'dept':dept,'year':year}
        b={'blog':blog,'title':title,'content':content,'author':author,'blogPic':blogPic}
        G={'Ground':Ground,'groundName':groundName,'NoOfCourt':NoOfCourt,'bookTime':bookTime}
        bk={'booking':booking,'GroundName':GroundName,'courtName':courtName,'date':date,'time':time}
        detail={'register':register,'b':b,'G':G,'bk':bk,'uData':None,'bb':None}
        if request.method == 'POST':
            if reg.validate_on_submit():
                email = reg.email.data
                role = reg.role.data
                dept = reg.dept.data
                year = reg.year.data
                dy=year+dept
                user=userInfo(email=email,role=role,dy=dy,password=password)
                db.session.add(user)
                db.session.commit()
                print(email,role,dy,password)
                

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
                bs=Blogs(title=title,content=content,author=author,mimetype=mimetype,image=img)
                db.session.add(bs)
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
                checkBook=Bookings.query.all()
                for x in checkBook:
                    if(x.ground==booking.groundName and x.courtName==booking.courtName.data and x.date==booking.date.data and x.time==booking.time.data):
                        print("Booking has been already made")
                        return render_template('gamesCouncillor-Dashboard.html',data={'g':'active','role_status': role_status,'bookings':_booking,'blogs':_blogs},detail=detail)
                GroundName=booking.groundName.data
                courtName=booking.courtName.data
                team_1=booking.team_1.data
                team_2=booking.team_2.data
                date=booking.date.data
                time=booking.time.data
                b=Bookings(ground=GroundName,courtName=courtName,team_1=team_1,team_2=team_2,date=date,time=time)
                db.session.add(b)
                db.session.commit()

                print(GroundName,courtName,team_1,team_2,date,time)
                booking.groundName.data=''
                booking.courtName.data=''
                booking.team_1.data=''
                booking.team_2.data=''
                booking.date.data=''
                booking.time.data=''
                return render_template('admin_page.html',detail=detail,data={'g':'active','role_status': session['LogAs'],'bookings':_booking,'blogs':_blogs})
            
        return render_template('admin_page.html',detail=detail,data={'g':'active','role_status': session['LogAs'],'bookings':_booking,'blogs':_blogs})
    else:
        return redirect(url_for('login'))

@app.route('/User-Dashboard', methods=['POST', 'GET'])
def studentDash():
    if "role" in session:
        GroundName=None
        courtName=None
        team_1=None
        team_2=None
        date=None
        time=None
        booking=f.BookingForm()
        g=Grounds.query.all()
        ground=[]
        for x in g:
            ground.append(x.groundName)
        booking.groundName.choices=ground
        booking.courtName.choices=func.court(3)
        booking.time.choices=func.schedule(1)
        booking.team_1.choices=course
        booking.team_2.choices=course
        booking.team_1.data=str(session['role'])
     #   _booking= db.session.execute(db.select(Bookings).filter(or_(Bookings.team_1.like(session['role']), Bookings.team_2.like(session['role'])))).scalars()
        nb=Bookings.query.all()
        _booking=[]
        for x in nb:
            y=int(x.team_1.find(session["role"]))+int(x.team_2.find(session["role"]))
            if(y==0):
                _booking.append(x)
     
        role=session['role']
        uData={'team_1':role}
        bk={'booking':booking,'GroundName':GroundName,'courtName':courtName,'date':date,'time':time}
        detail={'bk':bk,'uData':uData}
        if request.method == 'POST':
            if booking.validate_on_submit():
                checkBook=Bookings.query.all()
                for x in checkBook:
                    if(x.ground==booking.groundName and x.courtName==booking.courtName.data and x.date==booking.date.data and x.time==booking.time.data):
                        print("Booking has been already made")
                        return render_template('userDash.html',data={'g':'active','role_status': session['LogAs'],'bookings':_booking,},detail=detail)
                GroundName=booking.groundName.data
                courtName=booking.courtName.data
                team_1=booking.team_1.data
                team_2=booking.team_2.data
                date=booking.date.data
                time=booking.time.data
                print(GroundName,courtName,team_1,team_2,date,time)
                b=Bookings(ground=GroundName,courtName=courtName,team_1=team_1,team_2=team_2,date=date,time=time)
                db.session.add(b)
                db.session.commit()
                booking.groundName.data=''
                booking.courtName.data=''
                booking.team_1.data=''
                booking.team_2.data=''
                booking.date.data=''
                booking.time.data=''

        return render_template('userDash.html', data={'g':'active','role_status': session['LogAs'],'bookings':_booking},detail=detail)
    else:
        return redirect(url_for('login'))


@app.route('/aboutUs')
def aboutUs():
    return render_template('about_us.html', data={'e': 'active','role_status': session['LogAs']})


@app.route('/login', methods=['POST', 'GET'])
def login():
    email = None
    password = None
    form = f.LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            u=userInfo.query.all()
            email = form.email.data
            password = form.password.data
            for x in u:
                if(x.email==form.email.data and x.password==form.password.data):
                    session['role']=x.dy
                    session['email']=x.email
                    if(x.role=='Admin'):
                        session['LogAs']='Admin'
                        role_status=session['LogAs']

                        return redirect(url_for('admin'))
                    else:
                        session['LogAs']='User'
                        role_status=session['LogAs']
                        return redirect(url_for('studentDash'))

            
            form.email.data = ''
            form.password.data = ''
            print(email,password)

    return render_template('login.html', data={'f': 'active','n':'navitem' }, form=form, email=email, password=password)

def api():
    url = ('https://newsapi.org/v2/top-headlines?'
           'country=in'
           '&category=sports'
           '&apiKey=f36c80f9c4e041a48e37a202d089ea13')
    raesponse = requests.get(url)
    return raesponse.json()['articles']

@app.route("/logout")     
def logout():
    session.pop('role',None)
    session.pop('LogAs',None)
    session.pop('email', None)
    return redirect(url_for('login'))
    

if __name__ == "__main__":
    
    app.run(debug=True)
