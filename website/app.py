from flask import Flask, redirect, url_for, render_template, request
import http.client
import json
import requests
app = Flask(__name__)

@app.route('/')
def home():
    news=api()
    print(news[1]['title'])
    print('hello la')
    val={'news':news,'a':'active'}

    return render_template('home.html',data=val)

@app.route('/blog')
def blog():
    return render_template('blog.html',data={'b':'active'})

@app.route('/book')
def book():
    return render_template('book.html',data={'c':'active'})

@app.route('/booking')
def booking():
    return render_template('booking.html',data={'d':'active'})

@app.route('/gamesCouncillor-Dashboard')
def admin():
    return render_template('admin_page.html',data={})    

@app.route('/User-Dashboard')
def studentDash():
    return render_template('userDash.html',data={})   

@app.route('/aboutUs')
def aboutUs():
    return render_template('about_us.html',data={'e':'active'})


@app.route('/login')
def login():
    return render_template('login.html',data={'f':'active'})





def api():
    url = ('https://newsapi.org/v2/top-headlines?'
            'country=in'
            '&category=sports'
            '&apiKey=f36c80f9c4e041a48e37a202d089ea13')
    raesponse = requests.get(url)
    return raesponse.json()['articles']

if __name__ == "__main__":
    app.run(debug=True)     