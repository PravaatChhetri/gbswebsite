from flask import Flask, redirect, url_for, render_template, request
from flask_sqlalchemy import SQLAlchemy
import forms as f
import http.client
import json
import requests
app = Flask(__name__)
app.config['SECRET_KEY'] = 'groundbookingsystem'


@app.route('/')
def home():
    news = api()
    val = {'news': news, 'a': 'active'}
    return render_template('home.html', data=val)


@app.route('/blog')
def blog():
    return render_template('blog.html', data={'b': 'active'})


@app.route('/book')
def book():
    return render_template('book.html', data={'c': 'active'})


@app.route('/booking')
def booking():
    return render_template('booking.html', data={'d': 'active'})


@app.route('/gamesCouncillor-Dashboard', methods=['POST', 'GET'])
def admin():
    
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
    register={'reg':reg,'email':email,'role':role,'dept':dept,'year':year}
    b={'blog':blog,'title':title,'content':content,'author':author,'blogPic':blogPic}
    G={'Ground':Ground,'groundName':groundName,'NoOfCourt':NoOfCourt,'bookTime':bookTime}
    bk={'booking':booking,'GroundName':GroundName,'courtName':courtName,'date':date,'time':time}
    detail={'register':register,'b':b,'Ground':G,'booking':bk}
    if request.method == 'POST':
        if reg.validate_on_submit():
            email = reg.email.data
            role = reg.role.data
            dept = reg.dept.data
            year = reg.year.data
            
            reg.email.data=''
            reg.role.data=''
            reg.dept.data=''
            reg.year.data=''
            print(email,role,dept,year,password)
        if blog.validate_on_submit():
            title=blog.title.data
            content=blog.content.data
            author=blog.author.data
            blogPic=blog.upload.data
           
            print(title,content,author,blogPic)  
            blog.title.data=''
            blog.content.data=''
            blog.author.data=''
            blog.upload.data=''    
        if Ground.validate_on_submit():
            groundName=Ground.groundName.data
            NoOfCourt=Ground.NoOfCourt.data
            bookTime=Ground.bookTime.data
          
            print(groundName,NoOfCourt,bookTime)
            Ground.groundName.data=''
            Ground.NoOfCourt.data=''
            Ground.bookTime.data=''
        if booking.validate_on_submit():
            GroundName=booking.groundName.data
            courtName=booking.courtName.data
            date=booking.date.data
            time=booking.time.data
            
            print(GroundName,courtName,date,time)
            booking.groundName.data=''
            booking.courtName.data=''
            booking.date.data=''
            booking.time.data=''
        
    return render_template('admin_page.html',detail=detail,data={})


@app.route('/User-Dashboard')
def studentDash():
    return render_template('userDash.html', data={})


@app.route('/aboutUs')
def aboutUs():
    return render_template('about_us.html', data={'e': 'active'})


@app.route('/login', methods=['POST', 'GET'])
def login():
    email = None
    password = None
    form = f.LoginForm()
    if request.method == 'POST':
       
        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            form.email.data = ''
            form.password.data = ''
            print(email,password)

        # log_email=request.form['Lemail']
        # log_password=request.form['Lpass']
        # print(log_email)
        # print(log_password)

    return render_template('login.html', data={'f': 'active'}, form=form, email=email, password=password)


def api():
    url = ('https://newsapi.org/v2/top-headlines?'
           'country=in'
           '&category=sports'
           '&apiKey=f36c80f9c4e041a48e37a202d089ea13')
    raesponse = requests.get(url)
    return raesponse.json()['articles']


if __name__ == "__main__":
    app.run(debug=True)
